from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, form9_model, bat_info_model, issues_model
from ..forms import formE_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, createNotification

lock = login_required(login_url='Login')

back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formE(request, facility, fsID, selector):
    formName = 9
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.datetime.now().date()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    org = form9_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    full_name = request.user.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    
    # THIS IS TO TRANSITION THE MIGRATIONS NEED THIS TEMPORARILY ASK TOBE
    # for x in daily_prof:
    #     for y in bat_info_model.objects.all():
    #         if x.facility == y.facility_name:
    #             x.facilityChoice = y
    #             x.save()
    #             print('done')
    # for z in daily_prof:
    #     if "EES" in z.facility:
    #         z.facilityChoice = options
    #         z.save()

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            form = database_model
            existing = True
            search = True
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
            goose_neck_data_raw_JSON = json.loads(form.goose_neck_data)
            if len(goose_neck_data_raw_JSON) > 0:
                goose_neck_data_JSON = goose_neck_data_raw_JSON['data']
            else:
                goose_neck_data_JSON = ''
        else:
            if existing:
                initial_data = {
                    'observer': database_form.observer,
                    'date': database_form.date,
                    'crew': database_form.crew,
                    'foreman': database_form.foreman,
                    'start_time': database_form.start_time,
                    'end_time': database_form.end_time,
                    'leaks': database_form.leaks,
                    'goose_neck_data': database_form.goose_neck_data,
                }
                form = formE_form(initial=initial_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                }
                form = formE_form(initial=initial_data)
            goose_neck_data_JSON = ''
        if request.method == "POST":
            if existing:
                check = formE_form(request.POST, instance=database_form)
            else:
                check = formE_form(request.POST)

            A_valid = check.is_valid()

            if A_valid:
                A = check.save(commit=False)
                A.facilityChoice = options
                A.save()
                
                issueFound = False
                if not existing:
                    database_form = A
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
                if A.leaks == "Yes":
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
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formE.html", {
        'fsID': fsID, 
        'picker': picker, 
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        'existing': existing, 
        "back": back, 
        'todays_log': todays_log, 
        'form': form, 
        'selector': selector, 
        'profile': profile, 
        'formName': formName, 
        'leak_JSON': goose_neck_data_JSON, 
        'search': search, 
        'facility': facility,
        'notifs': notifs,
        'freq': freq
    })
