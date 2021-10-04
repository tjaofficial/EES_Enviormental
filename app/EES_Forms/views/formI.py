from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formI_model
from ..forms import formI_form

lock = login_required(login_url='Login')
now = datetime.datetime.now()
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formI(request, selector):
    formName = "I"
    existing = False
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    today = datetime.date.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_saturday + one_week
    today_number = today.weekday()
    week_start_dates = formI_model.objects.all().order_by('-week_start')
    opened = True
    submit = True
    filled_in = False
    week = ''
    week_almost = ''
    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector not in ('form', 'edit'):
            submit = False
            for x in week_start_dates:
                if str(x.week_start) == str(selector):
                    database_model = x
            empty_form = database_model
        elif len(week_start_dates) > 0:
            week_almost = week_start_dates[0]
            week = week_almost.week_start
            # ------- check if todays data has been filled in or not
            home = []

            for x in formI_model.objects.all():
                if x.week_start == last_saturday:
                    home.append((x.time_4, 4))
                    home.append((x.time_3, 3))
                    home.append((x.time_2, 2))
                    home.append((x.time_1, 1))
                    home.append((x.time_0, 0))
            for days in home:
                if days[0]:
                    if days[1] == today_number:
                        filled_in = True
            # -----check if today is a Weekday
            if today_number not in {5, 6}:
                # --------FORM------------FORM----------FORM-------------
                if selector == 'form':
                    if week == last_saturday:
                        if filled_in:
                            empty_form = week_almost
                            submit = False
                            existing = True
                # --------EDIT------------EDIT----------EDIT-------------
                elif selector == 'edit':
                    if week == last_saturday:
                        filled_in = False
                        existing = True
            elif today_number == 5:
                opened = False
                submit = False
                initial_data = {
                    'week_start': today,
                    'week_end': today + one_week
                }
                empty_form = formI_form(initial=initial_data)
            else:
                opened = False
                submit = False
                initial_data = {
                    'week_start': today - datetime.timedelta(days=1),
                    'week_end': today + one_week
                }
                empty_form = formI_form(initial=initial_data)
        if existing:
            initial_data = {
                'week_start': week_almost.week_start,
                'week_end': week_almost.week_end,
                'time_0': week_almost.time_0,
                'time_1': week_almost.time_1,
                'time_2': week_almost.time_2,
                'time_3': week_almost.time_3,
                'time_4': week_almost.time_4,
                'obser_0': week_almost.obser_0,
                'obser_1': week_almost.obser_1,
                'obser_2': week_almost.obser_2,
                'obser_3': week_almost.obser_3,
                'obser_4': week_almost.obser_4,
            }
            if filled_in:
                empty_form = week_almost
            else:
                empty_form = formI_form(initial=initial_data)
        else:
            initial_data = {
                'week_start': last_saturday,
                'week_end': end_week
            }
            empty_form = formI_form(initial=initial_data)

        if request.method == "POST":
            if existing:
                form = formI_form(request.POST, instance=week_almost)
            else:
                form = formI_form(request.POST)

            A_valid = form.is_valid()
            if A_valid:
                form.save()

                B = []
                for x in formI_model.objects.all():
                    if x.week_start == last_saturday:
                        B.append((4, x.time_4, x.obser_4))
                        B.append((3, x.time_3, x.obser_3))
                        B.append((2, x.time_2, x.obser_2))
                        B.append((1, x.time_1, x.obser_1))
                        B.append((0, x.time_0, x.obser_0))

                for days in B:
                    if days[0] == today_number:
                        if days[1] and days[2]:
                            filled_in = True
                        else:
                            filled_in = False

                if filled_in:
                    done = Forms.objects.filter(form='I')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formI.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'week': week, 'opened': opened, 'week_almost': week_almost, 'end_week': end_week, 'selector': selector, 'profile': profile, 'submit': submit, 'filled_in': filled_in, 'formName': formName
    })
