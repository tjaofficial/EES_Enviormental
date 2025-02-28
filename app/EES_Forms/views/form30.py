from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import issues_model, form_settings_model, daily_battery_profile_model, bat_info_model, form30_model
from ..forms import form30_form
from ..utils import updateSubmissionForm, createNotification, get_initial_data, checkIfFacilitySelected, getFacSettingsInfo, setUnlockClientSupervisor, issueForm_picker
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

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

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
        elif now == todays_log.date_save:
            if submitted_forms.exists():
                database_form = submitted_forms[0]
                if todays_log.date_save == database_form.date:
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
            data = form30_form(initial=initial_data)

        if request.method == "POST":
            print(request.POST)
            copyPOST = request.POST.copy()
            inspection_data = {
                "check1": {"status": request.POST.get("check1", ""), "comment": request.POST.get("comments1", "")},
                "check2": {"status": request.POST.get("check2", ""), "comment": request.POST.get("comments2", "")},
                "check3": {"status": request.POST.get("check3", ""), "comment": request.POST.get("comments3", "")},
                "check4": {"status": request.POST.get("check4", ""), "comment": request.POST.get("comments4", "")},
                "check5": {"status": request.POST.get("check5", ""), "comment": request.POST.get("comments5", "")},
                "check6": {"status": request.POST.get("check6", ""), "comment": request.POST.get("comments6", "")},
            }

            containers_data = {}
            index = 0
            while f"waste_description_{index}[]" in request.POST:
                containers_data[f"waste{index+1}"] = {
                    "description": request.POST.get(f"waste_description_{index}[]", ""),
                    "count": request.POST.get(f"container_count_{index}[]", ""),
                    "code": request.POST.get(f"waste_code_{index}[]", ""),
                    "dates": request.POST.getlist(f"waste_dates_{index}[]"),
                }
                index += 1
            copyPOST['inspection_json'] = inspection_data
            copyPOST['containers_json'] = containers_data
            # Create form instance and save
            form = form30_form(copyPOST)
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
        'fsID': fsID
    })