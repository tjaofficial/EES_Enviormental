from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import issues_model, user_profile_model, daily_battery_profile_model, Forms, form4_model, bat_info_model
from ..forms import formA4_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import json
from ..utils import issueForm_picker, checkIfFacilitySelected, updateSubmissionForm, setUnlockClientSupervisor, createNotification, getFacSettingsInfo

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

@lock
def formA4(request, facility, fsID, selector):
    formName = 4
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.datetime.now().date()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    org = form4_model.objects.all().order_by('-date')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            existing = True
            search = True
            print('CHECK 1')
        elif now == todays_log.date_save:
            if org.exists():
                database_form = org[0]
                if todays_log.date_save == database_form.date:
                    existing = True
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect(batt_prof)
        
        if search:
            database_form = ''
            leaks = ''
            collect_Raw_JSON = json.loads(data.leak_data)
            if len(collect_Raw_JSON) > 0:
                collect_json = collect_Raw_JSON['data']
            else:
                collect_json = ''
            
            if data.leak_data == '{}':
                leaks = 'no'
            elif data.leak_data == '':
                leaks = 'no data'
            else:
                leaks = 'yes'
        else:
            if existing:
                initial_data = {
                    'date': database_form.date,
                    'observer': database_form.observer,
                    'crew': database_form.crew,
                    'foreman': database_form.foreman,
                    'main_start': database_form.main_start,
                    'main_stop': database_form.main_stop,
                    'main_1': database_form.main_1,
                    'main_2': database_form.main_2,
                    'main_3': database_form.main_3,
                    'main_4': database_form.main_4,
                    'suction_main': database_form.suction_main,
                    'notes': database_form.notes,
                    'leak_data': database_form.leak_data,
                }
                if initial_data['leak_data'] == '{}':
                    leaks = 'no'
                else:
                    leaks = 'yes'
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'facility_name': facility,
                }
                leaks = 'no data'

            data = formA4_form(initial=initial_data)
            collect_json = ''
        
        if request.method == "POST":
            if existing:
                form = formA4_form(request.POST, instance=database_form)
            else:
                form = formA4_form(request.POST)
            finalFacility = options
            
            if form.is_valid():
                A = form.save(commit=False)
                A.facilityChoice = finalFacility
                if A.leak_data == '{"data":[]}':
                    A.leak_data = "{}"
                A.save()
                
                issueFound = False
                if not existing:
                    database_form = A
                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
                if A.notes.lower() != 'no ve' or A.leak_data != "{}":
                    issueFound = True
                if issueFound:
                    if finder:
                        if selector == 'form':
                            issue_page = 'resubmit'
                        else:
                            issue_page = 'issue'
                    else:
                        issue_page = 'form'
                    return redirect('issues_view', facility, fsID, str(database_form.date), issue_page)
                createNotification(facility, request, fsID, now, 'submitted', False)
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "shared/forms/daily/formA4.html", {
        'picker': picker, 
        'leaks': leaks,
        'collect_json': collect_json, 
        'options': options, 
        "search": search, 
        'existing': existing, 
        "client": client, 
        "supervisor": supervisor, 
        "back": back, 
        'todays_log': todays_log, 
        'data': data, 
        'formName': formName, 
        'profile': profile, 
        'selector': selector, 
        'unlock': unlock, 
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'fsID': fsID
    })
