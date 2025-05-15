from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import JsonResponse, HttpResponseRedirect# type: ignore
from ..models import form_settings_model, form30_model
from ..forms import form30_form
from ..utils.main_utils import get_initial_data, fix_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
from django.utils.timezone import now, timedelta # type: ignore

lock = login_required(login_url='Login')

@lock
def form30(request, fsID, selector):
    fix_data(fsID)
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, selector)
    facility = form_variables['facilityName']
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if request.user.user_profile.position == "observer": 
        if form_variables['daily_prof'].exists():
            todays_log = form_variables['daily_prof'][0]
        else:
            batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    else:
        todays_log = ""
    # -----SET DECIDING VARIABLES------------
    more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID) 
    if isinstance(more_form_variables, HttpResponseRedirect):
        return more_form_variables
    else:
        data, existing, search, database_form = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID)
    # -----SET RESPONSES TO DECIDING VARIABLES------------
    if search:
        database_form = ''
    else:
        if existing:
            unparsedData = get_initial_data(form30_model, database_form)
            inspection_initial = {}
            for i in range(1, 7):  # Assuming 6 status checks
                inspection_initial[f'check{i}'] = unparsedData["inspection_json"][f'check{i}']['status']
                inspection_initial[f'comments{i}'] = unparsedData["inspection_json"][f'check{i}']['comment']
            #print(inspection_initial)
            
            containers_initial = {}
            if "noContainers" not in unparsedData['containers_json'].keys():
                for index, (key, value) in enumerate(unparsedData['containers_json'].items()):
                    containers_initial[f'waste_description_{index}'] = value.get('description', "")
                    containers_initial[f'container_count_{index}'] = value.get('count', 0)
                    containers_initial[f'waste_code_{index}'] = value.get('code', "")

                    # Extract multiple dates
                    waste_dates = value.get('dates', [])
                    for date_idx, date_value in enumerate(waste_dates):
                        containers_initial[f'waste_dates_{index}_{date_idx}'] = date_value
            else:
                containers_initial['noContainers'] = False

            initial_data = unparsedData | inspection_initial
            initial_data["area_name"] = ""
        else:
            initial_data = {
                'date': todays_log.date_save,
                'observer': form_variables['full_name'],
                'formSettings': form_variables['freq'],
            }
        data = form30_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
    if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS------------
        copyPOST = request.POST.copy()

        try:
            form_settings = form_variables['freq']
        except form_settings_model.DoesNotExist:
            raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")

        copyPOST['formSettings'] = str(fsID)
        inspection_data = {
            "check1": {"status": request.POST.get("check1", ""), "comment": request.POST.get("comments1", "")},
            "check2": {"status": request.POST.get("check2", ""), "comment": request.POST.get("comments2", "")},
            "check3": {"status": request.POST.get("check3", ""), "comment": request.POST.get("comments3", "")},
            "check4": {"status": request.POST.get("check4", ""), "comment": request.POST.get("comments4", "")},
            "check5": {"status": request.POST.get("check5", ""), "comment": request.POST.get("comments5", "")},
            "check6": {"status": request.POST.get("check6", ""), "comment": request.POST.get("comments6", "")},
        }

        print(f"Here is Request.POST: {request.POST}")
        if "noContainers" in request.POST.keys():
            copyPOST['containers_json'] = {"noContainers": False}
        else:
            keyNumberList = []
            for key, formItem in request.POST.items():
                if 'waste_description' in key:
                    keyNumberList.append(key.replace("waste_description_", "").replace("[]", ""))
            print(keyNumberList)

            containers_data = {}
            index = 1
            for keyNumb in keyNumberList:
                containers_data[f"waste{index}"] = {
                    "description": request.POST.get(f"waste_description_{keyNumb}[]", ""),
                    "count": request.POST.get(f"container_count_{keyNumb}[]", ""),
                    "code": request.POST.get(f"waste_code_{keyNumb}[]", ""),
                    "dates": request.POST.getlist(f"waste_dates_{keyNumb}[]"),
                }
                index += 1
            copyPOST['containers_json'] = containers_data

        copyPOST['inspection_json'] = inspection_data
        
        start_of_week = form_variables['now'] - timedelta(days=form_variables['now'].weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        
        existing_form = form30_model.objects.filter(
            area_name=request.POST['area_name'],
            date__range=[start_of_week, end_of_week]
        ).first()
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
        if existing_form:
            if existing_form.area_name == database_form.area_name:
                print(f"Yes exisitng")
                form = form30_form(copyPOST, instance=database_form, form_settings=form_settings)
            else:
                form = form30_form(copyPOST, instance=existing_form, form_settings=form_settings)
        else:
            form = form30_form(copyPOST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
        exportVariables = (request, selector, facility, database_form, fsID)
        return redirect(*template_validate_save(form, form_variables, *exportVariables))
    return render(request, "shared/forms/weekly/form30.html", {
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'supervisor': form_variables['supervisor'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        "search": search, 
        'todays_log': todays_log, 
        'data': data, 
        'formName': form_variables['formName'], 
        'selector': selector,
        'picker': form_variables['picker'],
        'fsID': fsID,
        'existing': existing,
        'fsIDSelect': form_variables['fsIDSelect']
    })

def get_existing_form(request):
    area_name = request.GET.get("area_name")
    full_name = request.user.get_full_name()
    fsID = request.GET.get("fsID")
    if not area_name:
        return JsonResponse({"error": "No area name provided"}, status=400)
    # 🔥 Get the start and end of the current week
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    print(area_name)
    # 🔥 Search for an existing form within this week
    existing_form = form30_model.objects.filter(
        area_name=area_name,
        date__range=[start_of_week, end_of_week]
    ).first()
    print(existing_form)
    if existing_form:
        print("check 1")
        form_data = {
            "observer": existing_form.observer,
            "date": existing_form.date.strftime("%Y-%m-%d"),
            "time": existing_form.time.strftime("%H:%M"),
            "area_name": existing_form.area_name,
            "inspection_json": existing_form.inspection_json,  # Status Checks & Comments
            "containers_json": existing_form.containers_json,  # Waste Data
        }
        return JsonResponse({"form_data": form_data})
    else:
        new_form_data = {
            'date': today,
            'observer': full_name,
            #'formSettings': form_settings_model.objects.get(id=int(fsID)),
        }
        return JsonResponse({"new_form_data": new_form_data})

    return JsonResponse({"form_data": None})  # No existing form, return empty response

def get_submitted_areas(request):
    """Returns a list of area names that have been submitted this week."""
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    submitted_areas = form30_model.objects.filter(
        date__range=[start_of_week, end_of_week]
    ).values_list("area_name", flat=True).distinct()  # 🔥 Get unique area names

    return JsonResponse({"submitted_areas": list(submitted_areas)})



