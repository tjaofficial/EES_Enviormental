from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, issues_model, user_profile_model, daily_battery_profile_model, formP_model
from ..forms import formP_form
import calendar

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formP(request, selector, weekend_day):
    formName = "P"
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
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    today = datetime.date.today()
    full_name = request.user.get_full_name()

    month_name = calendar.month_name[today.month]

    org = formP_model.objects.all().order_by('-date')

    if weekend_day == 'saturday':
        ss_filler = 5
    elif weekend_day == 'sunday':
        ss_filler = 6
    else:
        ss_filler = ''

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            existing = True
            search = True
            unlock = False
        elif len(org) > 0:
            database_form = org[0]
            if database_form.date == today:
                existing = True
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'observer': database_form.observer,
                    'month': database_form.month,
                    'date': database_form.date,
                    'weekend_day': database_form.weekend_day,
                    'Q_1': database_form.Q_1,
                    'Q_2': database_form.Q_2,
                    'Q_3': database_form.Q_3,
                    'Q_4': database_form.Q_4,
                    'Q_5': database_form.Q_5,
                    'Q_6': database_form.Q_6,
                    'Q_7': database_form.Q_7,
                    'Q_8': database_form.Q_8,
                    'Q_9': database_form.Q_9,
                    'comments': database_form.comments,
                    'actions_taken': database_form.actions_taken,
                }
            else:
                initial_data = {
                    'date': today,
                    'observer': full_name,
                    'month': month_name,
                    'weekend_day': ss_filler,
                }
            data = formP_form(initial=initial_data)

        if request.method == 'POST':
            if existing:
                data = formP_form(request.POST, instance=database_form)
            else:
                data = formP_form(request.POST)
            A_valid = data.is_valid()
            if A_valid:
                A = data.save()

                if 'Yes' in {A.Q_2,A.Q_3,A.Q_4,A.Q_5,A.Q_6,A.Q_7,A.Q_8,A.Q_9}:
                    finder = issues_model.objects.filter(date=A.date, form='O')
                    if finder:
                        issue_page = '../../../issues_view/O/' + str(todays_log.date_save) + '/issue'
                    else:
                        issue_page = '../../../issues_view/O/' + str(todays_log.date_save) + '/form'

                    return redirect(issue_page)

                done = Forms.objects.filter(form='P')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formP.html", {
        'data': data, "search": search, "client": client, 'unlock': unlock, 'admin': admin, 'formName': formName, 'selector': selector, 'profile': profile, 'weekend_day': weekend_day
    })
