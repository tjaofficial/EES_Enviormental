from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formI_model, bat_info_model
from ..forms import formI_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

@lock
def formI(request, facility, selector):
    formName = "I"
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
    today = datetime.date.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_saturday + one_week
    today_number = today.weekday()
    week_start_dates = formI_model.objects.all().order_by('-week_start')
    opened = True
    submit = True
    filled_in = False
    partial_form = False
    week = ''
    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector not in ('form', 'edit'):
            submit = False
            for x in week_start_dates:
                if str(x.week_start) == str(selector):
                    print('CHECK 2')
                    database_model = x
            data = database_model
            existing = True
            search = True
            filled_in = True
        elif len(week_start_dates) > 0:
            print('CHECK 3')
            database_model = week_start_dates[0]
            week = database_model.week_start
            # ------- check if todays data has been filled in or not
            home = []

            for x in formI_model.objects.all():
                if x.week_start == last_saturday:
                    home.append((x.time_4, 4))
                    home.append((x.time_3, 3))
                    home.append((x.time_2, 2))
                    home.append((x.time_1, 1))
                    home.append((x.time_0, 0))
                    
            print(home)
            for days in home:
                if days[0]:
                    partial_form = True
                    if days[1] == today_number:
                        filled_in = True
            # -----check if today is a Weekday
            if today_number not in {5, 6}:
                print('CHECK 3.1')
                # --------FORM------------FORM----------FORM-------------
                if selector == 'form':
                    print(week)
                    print(last_saturday)
                    if week == last_saturday:
                        if filled_in or partial_form:
                            data = database_model
                            submit = False
                            existing = True
                # --------EDIT------------EDIT----------EDIT-------------
                elif selector == 'edit':
                    if week == last_saturday:
                        filled_in = False
                        existing = True
            elif today_number == 5:
                print('CHECK 3.2')
                opened = False
                submit = False
                initial_data = {
                    'week_start': today,
                    'week_end': today + one_week
                }
                data = formI_form(initial=initial_data)
            else:
                print('CHECK 3.3')
                opened = False
                submit = False
                initial_data = {
                    'week_start': today - datetime.timedelta(days=1),
                    'week_end': today + one_week
                }
                data = formI_form(initial=initial_data)
                
        if existing:
            print('Check 2.1')
            initial_data = {
                'week_start': database_model.week_start,
                'week_end': database_model.week_end,
                'time_0': database_model.time_0,
                'time_1': database_model.time_1,
                'time_2': database_model.time_2,
                'time_3': database_model.time_3,
                'time_4': database_model.time_4,
                'obser_0': database_model.obser_0,
                'obser_1': database_model.obser_1,
                'obser_2': database_model.obser_2,
                'obser_3': database_model.obser_3,
                'obser_4': database_model.obser_4,
            }
            if filled_in:
                data = database_model
            else:
                print('Check 2.2')
                data = formI_form(initial=initial_data)
        else:
            initial_data = {
                'week_start': last_saturday,
                'week_end': end_week
            }
            data = formI_form(initial=initial_data)
        print(data)
        print(database_model)
        if request.method == "POST":
            if existing:
                form = formI_form(request.POST, instance=database_model)
            else:
                form = formI_form(request.POST)

            A_valid = form.is_valid()
            if A_valid:
                form.save(commit=False)
                form.facilityChoice = options
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

                    return redirect('IncompleteForms', facility)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formI.html", {
        'facility': facility, "search": search, 'supervisor': supervisor, "back": back, 'todays_log': todays_log, 'empty': data, 'week': week, 'opened': opened, 'end_week': end_week, 'selector': selector, 'profile': profile, 'submit': submit, 'filled_in': filled_in, 'formName': formName, "client": client, 'unlock': unlock, 'partial': partial_form
    })
