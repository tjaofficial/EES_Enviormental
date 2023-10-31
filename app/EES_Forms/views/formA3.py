from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, user_profile_model, daily_battery_profile_model, Forms, formA3_model, bat_info_model
from ..forms import formA3_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import updateSubmissionForm, setUnlockClientSupervisor

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formA3(request, facility, selector):
    formName = 3
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    existing = False
    search = False
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    full_name = request.user.get_full_name()
    org = formA3_model.objects.all().order_by('-date')

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            existing = True
            search = True
        elif len(org) > 0:
            database_form = org[0]
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_form.date:
                        existing = True
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)

        if search:
            database_form = ''
            if data.om_leak_json:
                omSide_Raw_JSON = json.loads(data.om_leak_json)
                if len(omSide_Raw_JSON) > 0:
                    omSide_json = omSide_Raw_JSON['data']
                else:
                    omSide_json = ''
            else:
                omSide_json = ''
            if data.l_leak_json:
                lSide_Raw_JSON = json.loads(data.l_leak_json)
                if len(lSide_Raw_JSON) > 0:
                    lSide_json = lSide_Raw_JSON['data']
                else:
                    lSide_json = ''
            else:
                lSide_json = ''
        else:
            if existing:
                initial_data = {
                    'date': database_form.date,
                    'observer': database_form.observer,
                    'crew': database_form.crew,
                    'foreman': database_form.foreman,
                    'inop_ovens': database_form.inop_ovens,
                    'inop_numbs': database_form.inop_numbs,
                    'om_start': database_form.om_start,
                    'om_stop': database_form.om_stop,
                    'l_start': database_form.l_start,
                    'l_stop': database_form.l_stop,
                    'om_leak_json': database_form.om_leak_json,
                    'om_leaks2': database_form.om_leaks2,
                    'l_leak_json': database_form.l_leak_json,
                    'l_leaks2': database_form.l_leaks2,
                    'om_traverse_time_min': database_form.om_traverse_time_min,
                    'om_traverse_time_sec': database_form.om_traverse_time_sec,
                    'l_traverse_time_min': database_form.l_traverse_time_min,
                    'l_traverse_time_sec': database_form.l_traverse_time_sec,
                    'om_allowed_traverse_time': database_form.om_allowed_traverse_time,
                    'l_allowed_traverse_time': database_form.l_allowed_traverse_time,
                    'om_valid_run': database_form.om_valid_run,
                    'l_valid_run': database_form.l_valid_run,
                    'om_leaks': database_form.om_leaks,
                    'l_leaks': database_form.l_leaks,
                    'om_not_observed': database_form.om_not_observed,
                    'l_not_observed': database_form.l_not_observed,
                    'om_percent_leaking': database_form.om_percent_leaking,
                    'l_percent_leaking': database_form.l_percent_leaking,
                    'one_pass': database_form.one_pass,
                    'notes': database_form.notes,
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

            data = formA3_form(initial=initial_data)
            omSide_json = ''
            lSide_json = ''
        if request.method == "POST":
            if existing:
                form = formA3_form(request.POST, instance=database_form)
            else:
                form = formA3_form(request.POST)
            finalFacility = options
            
            if form.is_valid():
                A = form.save(commit=False)
                A.facilityChoice = finalFacility
                A.save()

                if A.notes not in {'-', 'n/a', 'N/A'} or int(A.om_leaks) > 0 or int(A.l_leaks) > 0:
                    finder = issues_model.objects.filter(date=A.date, form='A-3')
                    if finder:
                        issue_page = '../../issues_view/' + formName + '/' + str(database_form.date) + '/issue'
                    else:
                        issue_page = '../../issues_view/' + formName + '/' + str(database_form.date) + '/form'

                    return redirect(issue_page)

                updateSubmissionForm(facility, formName, True, todays_log.date_save)

                return redirect('IncompleteForms', facility)
            print(form)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA3.html", {
        'options': options, "unlock": unlock,"search": search, "supervisor": supervisor, "back": back, 'todays_log': todays_log, 'data': data, 'formName': formName, 'profile': profile, 'selector': selector, 'client': client, 'omSide_json': omSide_json, 'lSide_json': lSide_json, 'facility': facility
    })
