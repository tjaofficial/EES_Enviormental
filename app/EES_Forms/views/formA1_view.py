from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, daily_battery_profile_model, formA1_model, formA1_readings_model, Forms, bat_info_model
from ..forms import formA1_form, formA1_readings_form


lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formA1(request, facility, selector):
    formName = "A1"
    existing = False
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
    now = datetime.datetime.now()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    org = formA1_model.objects.all().order_by('-date')
    org2 = formA1_readings_model.objects.all().order_by('-form')

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        print('CHECK 1')
        todays_log = daily_prof[0]
        print('CHECK 2')
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            for x in org2:
                if str(x.form.date) == str(selector):
                    database_model2 = x
            readings = database_model2
            existing = True
            search = True
        elif len(org) > 0 and len(org2) > 0:
            database_form = org[0]
            database_form2 = org2[0]

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
        else:
            if existing:
                initial_data = {
                    'date': database_form.date,
                    'observer': database_form.observer,
                    'crew': database_form.crew,
                    'foreman': database_form.foreman,
                    'start': database_form.start,
                    'stop': database_form.stop,
                    'c1_no': database_form2.c1_no,
                    'c2_no': database_form2.c2_no,
                    'c3_no': database_form2.c3_no,
                    'c4_no': database_form2.c4_no,
                    'c5_no': database_form2.c5_no,
                    'c1_start': database_form2.c1_start,
                    'c2_start': database_form2.c2_start,
                    'c3_start': database_form2.c3_start,
                    'c4_start': database_form2.c4_start,
                    'c5_start': database_form2.c5_start,
                    'c1_stop': database_form2.c1_stop,
                    'c2_stop': database_form2.c2_stop,
                    'c3_stop': database_form2.c3_stop,
                    'c4_stop': database_form2.c4_stop,
                    'c5_stop': database_form2.c5_stop,
                    'c1_sec': database_form2.c1_sec,
                    'c2_sec': database_form2.c2_sec,
                    'c3_sec': database_form2.c3_sec,
                    'c4_sec': database_form2.c4_sec,
                    'c5_sec': database_form2.c5_sec,
                    'c1_comments': database_form2.c1_comments,
                    'c2_comments': database_form2.c2_comments,
                    'c3_comments': database_form2.c3_comments,
                    'c4_comments': database_form2.c4_comments,
                    'c5_comments': database_form2.c5_comments,
                    'larry_car': database_form2.larry_car,
                    'comments': database_form2.comments,
                    'total_seconds': database_form2.total_seconds,
                }
                readings = formA1_readings_form(initial=initial_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                }
                readings = formA1_readings_form()

            data = formA1_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formA1_form(request.POST, instance=database_form)
                reads = formA1_readings_form(request.POST, instance=database_form2)
            else:
                form = formA1_form(request.POST)
                reads = formA1_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = reads.is_valid()

            if A_valid and B_valid:
                A = form.save()
                B = reads.save(commit=False)
                B.form = A
                B.save()

                finder = issues_model.objects.filter(date=A.date, form='A-1')
            #     if B.comments not in {'-', 'n/a', 'N/A'}:
            #         issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

            #         return redirect (issue_page)
                sec = {B.c1_sec, B.c2_sec, B.c3_sec, B.c4_sec, B.c5_sec}
                for x in sec:
                    if 10 <= x:
                        if finder:
                            issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/issue'
                        else:
                            issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

                        return redirect(issue_page)
                    else:
                        if B.total_seconds >= 55:
                            if finder:
                                issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/issue'
                            else:
                                issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

                            return redirect(issue_page)
                done = Forms.objects.filter(form='A-1')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms', facility)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA1.html", {
        "search": search, 'admin': admin, "back": back, 'todays_log': todays_log, 'data': data, 'readings': readings, 'formName': formName, 'selector': selector, "client": client, 'unlock': unlock, 'facility': facility
    })


    hourNum = int(str(time)[0:2])
    minNum = str(time)[3:5]
    timeLabel = 'AM'
    if hourNum > 12:
        newHourNum = str(hourNum - 12)
        timeLabel = 'PM'
        newTime = newHourNum + ':' + minNum + ' ' + timeLabel
    elif hourNum == 00:
        newHourNum = '12'
        newTime = newHourNum + ':' + minNum + ' ' + timeLabel
    else:
        newTime = str(hourNum) + ':' + minNum + ' ' + timeLabel
    return newTime