from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, user_profile_model, daily_battery_profile_model, Forms, formA2_model, bat_info_model
from ..forms import formA2_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import issueForm_picker,updateSubmissionForm,setUnlockClientSupervisor, createNotification

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formA2(request, facility, fsID, selector):
    formName = 2
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    search = False
    existing = False
    now = datetime.datetime.now().date()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    full_name = request.user.get_full_name()
    org = formA2_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
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
                initial_data = {
                    'date': database_form.date,
                    'observer': database_form.observer,
                    'crew': database_form.crew,
                    'foreman': database_form.foreman,
                    'inop_ovens': database_form.inop_ovens,
                    'inop_numbs': database_form.inop_numbs,
                    'p_start': database_form.p_start,
                    'p_stop': database_form.p_stop,
                    'c_start': database_form.c_start,
                    'c_stop': database_form.c_stop,
                    'p_leak_data': database_form.p_leak_data,
                    'c_leak_data': database_form.c_leak_data,
                    'notes': database_form.notes,
                    'p_temp_block_from': database_form.p_temp_block_from,
                    'p_temp_block_to': database_form.p_temp_block_to,
                    'c_temp_block_from': database_form.c_temp_block_from,
                    'c_temp_block_to': database_form.c_temp_block_to,
                    'p_traverse_time_min': database_form.p_traverse_time_min,
                    'p_traverse_time_sec': database_form.p_traverse_time_sec,
                    'c_traverse_time_min': database_form.c_traverse_time_min,
                    'c_traverse_time_sec': database_form.c_traverse_time_sec,
                    'total_traverse_time': database_form.total_traverse_time,
                    'allowed_traverse_time': database_form.allowed_traverse_time,
                    'valid_run': database_form.valid_run,
                    'leaking_doors': database_form.leaking_doors,
                    'doors_not_observed': database_form.doors_not_observed,
                    'inop_doors_eq': database_form.inop_doors_eq,
                    'percent_leaking': database_form.percent_leaking,
                }
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
                A.save()
                
                issueFound = False
                compliance = False
                if not existing:
                    database_form = A
                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
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
                createNotification(facility, request.user, fsID, now, 'submitted')
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
        "back": back, 
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