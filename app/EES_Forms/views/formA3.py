from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import user_profile_model, daily_battery_profile_model, Forms, formA3_model
from ..forms import formA3_form

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')
now = datetime.datetime.now()


@lock
def formA3(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    formName = "A3"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    org = formA3_model.objects.all().order_by('-date')
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
                            'inop_ovens': database_form.inop_ovens,
                            'om_start': database_form.om_start,
                            'om_stop': database_form.om_stop,
                            'l_start': database_form.l_start,
                            'l_stop': database_form.l_stop,
                            'om_oven1': database_form.om_oven1,
                            'om_loc1': database_form.om_loc1,
                            'l_oven1': database_form.l_oven1,
                            'l_loc1': database_form.l_loc1,
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
                            'notes': database_form.notes,
                        }
                        data = formA3_form(initial=initial_data)
                        if request.method == "POST":
                            form = formA3_form(request.POST, instance=database_form)
                            if form.is_valid():
                                A = form.save()

                                if A.notes not in {'-', 'n/a', 'N/A'}:
                                    issue_page = '../../issues_view/A-3/' + str(database_form.date) + '/form'

                                    return redirect(issue_page)
                                if int(A.om_leaks) > 0:
                                    issue_page = '../../issues_view/A-3/' + str(database_form.date) + '/form'

                                    return redirect(issue_page)
                                if int(A.l_leaks) > 0:
                                    issue_page = '../../issues_view/A-3/' + str(database_form.date) + '/form'

                                    return redirect(issue_page)

                                done = Forms.objects.filter(form='A-3')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')

                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name,
                            'crew': todays_log.crew,
                            'foreman': todays_log.foreman,
                            'inop_ovens': todays_log.inop_ovens,
                            'notes': 'N/A',
                        }
                        data = formA3_form(initial=initial_data)
                        if request.method == "POST":
                            form = formA3_form(request.POST)
                            if form.is_valid():
                                A = form.save()

                                if A.notes not in {'-', 'n/a', 'N/A'}:
                                    issue_page = '../../issues_view/A-3/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)
                                if int(A.om_leaks) > 0:
                                    issue_page = '../../issues_view/A-3/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)
                                if int(A.l_leaks) > 0:
                                    issue_page = '../../issues_view/A-3/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)

                                done = Forms.objects.filter(form='A-3')[0]
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

    return render(request, "Daily/formA3.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'formName': formName, 'profile': profile, 'selector': selector, 'client': client,
    })
