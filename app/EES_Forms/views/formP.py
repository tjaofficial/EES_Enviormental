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

    if formP_model.objects.count() != 0:
        database_form = org[0]
        database_date = database_form.date
    else:
        database_date = ''

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data_form = database_model
        else:
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_date:
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
                        data_form = formP_form(initial=initial_data)

                        if request.method == 'POST':
                            data_form = formP_form(request.POST, instance=database_form)
                            if data_form.is_valid():
                                A = data_form.save()

                                if 'Yes' in {
                                    A.Q_2,
                                    A.Q_3,
                                    A.Q_4,
                                    A.Q_5,
                                    A.Q_6,
                                    A.Q_7,
                                    A.Q_8,
                                    A.Q_9,
                                }:
                                    issue_page = '../../../issues_view/P/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)

                                done = Forms.objects.filter(form='P')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': today,
                            'observer': full_name,
                            'month': month_name,
                            'weekend_day': ss_filler,
                        }
                        data_form = formP_form(initial=initial_data)

                        if request.method == 'POST':
                            data_form = formP_form(request.POST)
                            if data_form.is_valid():
                                A = data_form.save()

                                if 'Yes' in {
                                    A.Q_2,
                                    A.Q_3,
                                    A.Q_4,
                                    A.Q_5,
                                    A.Q_6,
                                    A.Q_7,
                                    A.Q_8,
                                    A.Q_9,
                                }:
                                    finder = issues_model.objects.filter(date=A.date, form='P')
                                    if finder:
                                        issue_page = '../../../issues_view/P/' + str(todays_log.date_save) + '/issue'
                                    else:
                                        issue_page = '../../../issues_view/P/' + str(todays_log.date_save) + '/form'

                                    return redirect(issue_page)

                                done = Forms.objects.filter(form='P')[0]
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

    return render(request, "Weekly/formP.html", {
        'selector': selector, 'profile': profile, 'data_form': data_form, 'weekend_day': weekend_day
    })
