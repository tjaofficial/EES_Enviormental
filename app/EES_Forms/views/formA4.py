from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, user_profile_model, daily_battery_profile_model, Forms, formA4_model, bat_info_model
from ..forms import formA4_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import json

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

@lock
def formA4(request, facility, selector):
    formName = "A4"
    existing = False
    unlock = False
    client = False
    search = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    org = formA4_model.objects.all().order_by('-date')
    
    count_bp = daily_battery_profile_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    if count_bp != 0:
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
            collect_Raw_JSON = json.loads(data.leak_data)
            if len(collect_Raw_JSON) > 0:
                collect_json = collect_Raw_JSON['data']
            else:
                collect_json = ''
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
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'facility_name': facility,
                }

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
                if A.notes.lower() != 'no ve' or A.leak_data != "{}":
                    finder = issues_model.objects.filter(date=A.date, form='A-4')
                    if finder:
                        issue_page = '../../issues_view/A-4/' + str(todays_log.date_save) + '/issue'
                    else:
                        issue_page = '../../issues_view/A-4/' + str(todays_log.date_save) + '/form'
                
                    return redirect(issue_page)
                elif issues_model.objects.filter(date=A.date, form='A-4'):
                    issues_model.objects.filter(date=A.date, form='A-4')[0].delete()
                
                done = Forms.objects.filter(form='A-4')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms', facility)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA4.html", {
        'collect_json': collect_json, 'options': options, "search": search, 'existing': existing, "client": client, "supervisor": supervisor, "back": back, 'todays_log': todays_log, 'data': data, 'formName': formName, 'profile': profile, 'selector': selector, 'unlock': unlock, 'facility': facility
    })
