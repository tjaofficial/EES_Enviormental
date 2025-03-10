from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import issues_model, form_settings_model, daily_battery_profile_model, bat_info_model, form30_model
from ..forms import form30_form
from ..utils import updateSubmissionForm, createNotification, get_initial_data, checkIfFacilitySelected, getFacSettingsInfo, setUnlockClientSupervisor, issueForm_picker
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import json
from django.http import JsonResponse # type: ignore
from django.utils.timezone import now, timedelta # type: ignore

lock = login_required(login_url='Login')

@lock
def form30(request, facility, fsID, selector):
    formName = 30
    notifs = checkIfFacilitySelected(request.user, facility)
    freq = getFacSettingsInfo(fsID)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    submitted_forms = form30_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    fsIDSelect = form_settings_model.objects.get(id=int(fsID))

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
        elif now == todays_log.date_save:
            database_form = submitted_forms[0] if submitted_forms.exists() else False
            if database_form and todays_log.date_save == database_form.date:
                existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    
        if search:
            database_form = ''
        else:
            if existing:
                unparsedData = get_initial_data(form30_model, database_form)
                inspection_initial = {}
                for i in range(1, 7):  # Assuming 6 status checks
                    inspection_initial[f'check{i}'] = unparsedData["inspection_json"][f'check{i}']['status']
                    inspection_initial[f'comments{i}'] = unparsedData["inspection_json"][f'check{i}']['comment']
                print(inspection_initial)
                
                containers_initial = {}
                for index, (key, value) in enumerate(unparsedData['containers_json'].items()):
                    containers_initial[f'waste_description_{index}'] = value.get('description', "")
                    containers_initial[f'container_count_{index}'] = value.get('count', 0)
                    containers_initial[f'waste_code_{index}'] = value.get('code', "")

                    # Extract multiple dates
                    waste_dates = value.get('dates', [])
                    for date_idx, date_value in enumerate(waste_dates):
                        containers_initial[f'waste_dates_{index}_{date_idx}'] = date_value

                initial_data = unparsedData | inspection_initial
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'formSettings': form_settings_model.objects.get(id=int(fsID)),
                }
            data = form30_form(initial=initial_data, form_settings=fsIDSelect)

        if request.method == "POST":
            print(request.POST)
            copyPOST = request.POST.copy()

            try:
                form_settings = fsIDSelect
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

            copyPOST['inspection_json'] = inspection_data
            copyPOST['containers_json'] = containers_data
            
            start_of_week = now - timedelta(days=now.weekday())  # Monday
            end_of_week = start_of_week + timedelta(days=6)  # Sunday
            
            existing_form = form30_model.objects.filter(
                area_name=request.POST['area_name'],
                date__range=[start_of_week, end_of_week]
            ).first()
            
            # Create form instance and save
            if existing_form:
                if existing_form.area_name == database_form.area_name:
                    print(f"Yes exisitng")
                    form = form30_form(copyPOST, instance=database_form, form_settings=form_settings)
                else:
                    form = form30_form(copyPOST, instance=existing_form, form_settings=form_settings)
            else:
                form = form30_form(copyPOST, form_settings=form_settings)

            print(form.errors)
            if form.is_valid():
                print("saved")
                A = form.save(commit=False)
                A.formSettings = form_settings_model.objects.get(id=int(fsID))
                A.facilityChoice = options
                A.save()

                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, formChoice=A.formSettings).exists()
                #INSERT ANY CHECKS HERE
                issueFound = False
                compliance = False
                if issueFound:
                    if finder:
                        if selector == 'form':
                            issue_page = 'resubmit'
                        else:
                            issue_page = 'issue'
                    else:
                        issue_page = 'form'
                    
                    if compliance:
                        issue_page = issue_page + "-c"
                        
                    return redirect('issues_view', facility, fsID, str(database_form.date), issue_page)


                createNotification(facility, request, fsID, now, 'submitted', False)        
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)


    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    return render(request, "shared/forms/weekly/form30.html", {
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'options': options, 
        "search": search, 
        'todays_log': todays_log, 
        'data': data, 
        'formName': formName, 
        'selector': selector,
        'picker': picker,
        'fsID': fsID,
        'existing': existing,
        "database_form": database_form
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



