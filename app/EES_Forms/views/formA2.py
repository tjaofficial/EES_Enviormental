from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import user_profile_model, daily_battery_profile_model, Forms, formA2_model
from ..forms import formA2_form
import json

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formA2(request, selector):
    unlock = False
    client = False
    search = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    formName = "A2"
    existing = False
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    full_name = request.user.get_full_name()
    count_bp = daily_battery_profile_model.objects.count()
    org = formA2_model.objects.all().order_by('-date')

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
            pSide_Raw_JSON = json.loads(data.p_leak_data)
            cSide_Raw_JSON = json.loads(data.c_leak_data)
            pSide_json = pSide_Raw_JSON['data']
            cSide_json = cSide_Raw_JSON['data']
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
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'inop_ovens': todays_log.inop_ovens,
                    'inop_numbs': todays_log.inop_numbs,
                    'notes': 'N/A',
                }

            data = formA2_form(initial=initial_data)
            pSide_json = ''
            cSide_json = ''
            
        if request.method == "POST":
            if existing:
                form = formA2_form(request.POST, instance=database_form)
            else:
                form = formA2_form(request.POST)

            if form.is_valid():
                A = form.save()

                if A.notes not in {'-', 'n/a', 'N/A'}:
                    issue_page = '../../issues_view/A-2/' + str(database_form.date) + '/form'

                    return redirect(issue_page)

                if A.leaking_doors == 0:
                    done = Forms.objects.filter(form='A-2')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()
                    print("nigga we made it")
                    return redirect('IncompleteForms')
                else:
                    issue_page = '../../issues_view/A-2/' + str(database_form.date) + '/form'

                    return redirect(issue_page)
            else:
                print("Form not valid")
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA2.html", {
        "unlock": unlock, 'admin': admin, "back": back, 'todays_log': todays_log, 'data': data, 'formName': formName, 'profile': profile, 'selector': selector, 'client': client, "pSide_json": pSide_json, 'cSide_json': cSide_json,
    })
