from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import user_profile_model, daily_battery_profile_model, Forms, formA4_model
from ..forms import formA4_form

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')
now = datetime.datetime.now()


@lock
def formA4(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    formName = "A4"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    org = formA4_model.objects.all().order_by('-date')
    database_form = org[0]

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model

        else:
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_form.date:
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
                            'oven_leak_1': database_form.oven_leak_1,
                            'time_leak_1': database_form.time_leak_1,
                            'date_temp_seal_leak_1': database_form.date_temp_seal_leak_1,
                            'time_temp_seal_leak_1': database_form.time_temp_seal_leak_1,
                            'temp_seal_by_leak_1': database_form.temp_seal_by_leak_1,
                            'date_init_repair_leak_1': database_form.date_init_repair_leak_1,
                            'time_init_repair_leak_1': database_form.time_init_repair_leak_1,
                            'date_comp_repair_leak_1': database_form.date_comp_repair_leak_1,
                            'time_comp_repair_leak_1': database_form.time_comp_repair_leak_1,
                            'comp_by_leak_1': database_form.comp_by_leak_1,
                            'notes': database_form.notes,
                        }
                        data = formA4_form(initial=initial_data)

                        if request.method == "POST":
                            form = formA4_form(request.POST, instance=database_form)
                            if form.is_valid():
                                A = form.save()

                                if A.notes not in {'No VE', 'NO VE', 'no ve', 'no VE'}:
                                    issue_page = '../../issues_view/A-4/' + str(database_form.date) + '/form'

                                    return redirect(issue_page)
                                if A.oven_leak_1:
                                    issue_page = '../../issues_view/A-4/' + str(database_form.date) + '/form'

                                    return redirect(issue_page)

                                done = Forms.objects.filter(form='A-4')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                            else:
                                print(form.errors)

                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name,
                            'crew': todays_log.crew,
                            'foreman': todays_log.foreman,
                        }
                        data = formA4_form(initial=initial_data)

                        if request.method == "POST":
                            form = formA4_form(request.POST)
                            if form.is_valid():
                                A = form.save()

                                if A.notes not in {'No VE', 'NO VE', 'no ve', 'no VE'}:
                                    issue_page = '../../issues_view/A-4/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)
                                if A.oven_leak_1:
                                    issue_page = '../../issues_view/A-4/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)

                                done = Forms.objects.filter(form='A-4')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA4.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'formName': formName, 'profile': profile, 'selector': selector, 'client': client,
    })
