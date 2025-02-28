from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import form_settings_model, issues_model, user_profile_model, daily_battery_profile_model, Forms, form2_model, bat_info_model
from ..forms import formA2_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, createNotification, checkIfFacilitySelected, getFacSettingsInfo, get_initial_data

lock = login_required(login_url='Login')



@lock
def formA2(request, facility, fsID, selector):
    formName = 2
    notifs = checkIfFacilitySelected(request.user, facility)
    freq = getFacSettingsInfo(fsID)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    submitted_forms = form2_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    profile = user_profile_model.objects.all()
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
            pSide_Raw_JSON = json.loads(data.p_leak_data)
            cSide_Raw_JSON = json.loads(data.c_leak_data)
            if len(pSide_Raw_JSON) > 0:
                pSide_json = pSide_Raw_JSON['data']
            else:
                pSide_json = ''
            if len(cSide_Raw_JSON) > 0:
                cSide_json = cSide_Raw_JSON['data']
            else:
                cSide_json = ''
        else:
            if existing:
                initial_data = get_initial_data(form2_model, database_form)
            else:
                inopNumbsParse = todays_log.inop_numbs.replace("'","").replace("[","").replace("]","")
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'inop_ovens': todays_log.inop_ovens,
                    'inop_numbs': inopNumbsParse,
                    'notes': 'N/A',
                    'facility_name': facility,
                }
            data = formA2_form(initial=initial_data)
            pSide_json = ''
            cSide_json = ''
        if request.method == "POST":
            if existing:
                form = formA2_form(request.POST, instance=database_form)
            else:
                form = formA2_form(request.POST)
            finalFacility = options
            if form.is_valid():
                A = form.save(commit=False)
                A.facilityChoice = finalFacility
                A.formSettings = form_settings_model.objects.get(id=int(fsID))
                A.save()
                
                issueFound = False
                compliance = False
                if not existing:
                    database_form = A
                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, formChoice=A.formSettings).exists()
                print(issues_model.objects.filter(date=A.date, formChoice=A.formSettings))
                if A.notes not in {'-', 'n/a', 'N/A'} or A.leaking_doors != 0:
                    issueFound = True
                    if A.leaking_doors > 8:
                        compliance = True
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
                print("Form not valid")
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    return render(request, "shared/forms/daily/formA2.html", {
        'picker': picker, 
        'options': options, 
        "search": search, 
        "unlock": unlock, 
        'supervisor': supervisor, 
        'notifs': notifs,
        'freq': freq,
         
        'todays_log': todays_log, 
        'data': data, 
        'formName': formName, 
        'profile': profile, 
        'selector': selector, 
        'client': client, 
        "pSide_json": pSide_json, 
        'cSide_json': cSide_json, 
        'facility': facility,
        'fsID': fsID
    })