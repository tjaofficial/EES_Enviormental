from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import user_profile_model, daily_battery_profile_model, Forms, formA2_model
from ..forms import formA2_form

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')
now = datetime.datetime.now()


@lock
def formA2(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    formName = "A2"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    org = formA2_model.objects.all().order_by('-date')

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model

        elif len(org) > 0:
            database_form = org[0]

            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'date': database_form.date,
                            'observer': database_form.observer,
                            'crew': database_form.crew,
                            'foreman': database_form.foreman,
                            'inop_ovens': database_form.inop_ovens,
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
                        data = formA2_form(initial=initial_data)
                        if request.method == "POST":
                            form = formA2_form(request.POST, instance=database_form)
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

                                    return redirect('IncompleteForms')
                                else:
                                    issue_page = '../../issues_view/A-2/' + str(database_form.date) + '/form'

                                    return redirect(issue_page)
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name,
                            'crew': todays_log.crew,
                            'foreman': todays_log.foreman,
                            'inop_ovens': todays_log.inop_ovens,
                            'notes': 'N/A',
                        }
                        data = formA2_form(initial=initial_data)
                        if request.method == "POST":
                            form = formA2_form(request.POST)
                            if form.is_valid():
                                A = form.save()

                                if A.notes not in {'-', 'n/a', 'N/A'}:
                                    issue_page = '../../issues_view/A-2/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)

                                if A.leaking_doors == 0:
                                    done = Forms.objects.filter(form='A-2')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                                else:
                                    issue_page = '../../issues_view/A-2/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name,
                'crew': todays_log.crew,
                'foreman': todays_log.foreman,
                'inop_ovens': todays_log.inop_ovens,
                'notes': 'N/A',
            }
            data = formA2_form(initial=initial_data)
            if request.method == "POST":
                form = formA2_form(request.POST)
                if form.is_valid():
                    A = form.save()

                    if A.notes not in {'-', 'n/a', 'N/A'}:
                        issue_page = '../../issues_view/A-2/' + str(todays_log.date_save) + '/form'

                        return redirect(issue_page)

                    if A.leaking_doors == 0:
                        done = Forms.objects.filter(form='A-2')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
                    else:
                        issue_page = '../../issues_view/A-2/' + str(todays_log.date_save) + '/form'

                        return redirect(issue_page)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA2.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'formName': formName, 'profile': profile, 'selector': selector, 'client': client,
    })