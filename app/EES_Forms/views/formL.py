from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formL_model
from ..forms import formL_form

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formL(request, access_page):
    formName = "L"
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
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    today = datetime.date.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_saturday + one_week
    today_number = today.weekday()
    opened = True
    count_bp = daily_battery_profile_model.objects.count()
    week_start_dates = formL_model.objects.all().order_by('-week_start')

    # -----check if Daily Battery Profile
    if count_bp != 0:
        todays_log = daily_prof[0]
        # -------check if access is for Form or Edit
        if access_page not in ('form', 'edit'):
            for x in week_start_dates:
                if str(x.week_start) == str(access_page):
                    database_model = x
                    filled_in = True
            empty_form = database_model
        # -----check if database is empty
        elif len(week_start_dates) > 0:
            week_almost = week_start_dates[0]
            this_week_saturday = week_almost.week_start
            database = week_almost
            
            # -----check if the days data has been filled in
            home = []
            filled_in = False
            for x in formL_model.objects.all():
                ## print(last_saturday)
                if x.week_start == last_saturday:
                    home.append((x.time_4, 4))
                    home.append((x.time_3, 3))
                    home.append((x.time_2, 2))
                    home.append((x.time_1, 1))
                    home.append((x.time_0, 0))
                    home.append((x.time_6, 6))
                    home.append((x.time_5, 5))
            for days in home:
                if days[0]:
                    if days[1] == today_number:
                        filled_in = True
            # ------check if today is a Weekday
            if today_number not in {5, 6}:
                new_saturday = ''
                new_sunday = ''
                # ---------- FORM ----------- FORM -------------- FORM ----------
                if access_page == 'form':
                    if this_week_saturday == last_saturday:
                        existing = True
                # ---------- EDIT ----------- EDIT -------------- EDIT ----------
                elif access_page == "edit":
                    if this_week_saturday == last_saturday:
                        existing = True
                        filled_in = False
            # ------check if today is a Saturday
            elif today_number == 5:
                # ---------- FORM ----------- FORM -------------- FORM ----------
                if access_page == 'form':
                    if this_week_saturday == today:
                        existing = True
                    else:
                        new_saturday = True
                        new_sunday = ''
                # ---------- EDIT ----------- EDIT -------------- EDIT ----------
                elif access_page == "edit":
                    if this_week_saturday == today:
                        existing = True
                        filled_in = False
                    else:
                        print('error - Editing a form that does not exist in the data base')
            # ----if today is a Sunday-------
            else:
                # ---------- FORM ----------- FORM -------------- FORM ----------
                if access_page == 'form':
                    sunday_last_sat = today - datetime.timedelta(days=1)
                    if this_week_saturday == sunday_last_sat:
                        existing = True
                    else:
                        new_sunday = True
                        new_saturday = ''
                        
                # ---------- EDIT ----------- EDIT -------------- EDIT ----------
                elif access_page == "edit":
                    sunday_last_sat = today - datetime.timedelta(days=1)
                    if this_week_saturday == sunday_last_sat:
                        existing = True
                        filled_in = False
                    else:
                        print('error - Editing a form that does not exist in the data base')
        if existing:
            initial_data = {
                'week_start': database.week_start,
                'week_end': database.week_end,
                'time_0': database.time_0,
                'obser_0': database.obser_0,
                'vents_0': database.vents_0,
                'mixer_0': database.mixer_0,
                'v_comments_0': database.v_comments_0,
                'm_comments_0': database.m_comments_0,
                'time_1': database.time_1,
                'obser_1': database.obser_1,
                'vents_1': database.vents_1,
                'mixer_1': database.mixer_1,
                'v_comments_1': database.v_comments_1,
                'm_comments_1': database.m_comments_1,
                'time_2': database.time_2,
                'obser_2': database.obser_2,
                'vents_2': database.vents_2,
                'mixer_2': database.mixer_2,
                'v_comments_2': database.v_comments_2,
                'm_comments_2': database.m_comments_2,
                'time_3': database.time_3,
                'obser_3': database.obser_3,
                'vents_3': database.vents_3,
                'mixer_3': database.mixer_3,
                'v_comments_3': database.v_comments_3,
                'm_comments_3': database.m_comments_3,
                'time_4': database.time_4,
                'obser_4': database.obser_4,
                'vents_4': database.vents_4,
                'mixer_4': database.mixer_4,
                'v_comments_4': database.v_comments_4,
                'm_comments_4': database.m_comments_4,
                'time_5': database.time_5,
                'obser_5': database.obser_5,
                'vents_5': database.vents_5,
                'mixer_5': database.mixer_5,
                'v_comments_5': database.v_comments_5,
                'm_comments_5': database.m_comments_5,
                'time_6': database.time_6,
                'obser_6': database.obser_6,
                'vents_6': database.vents_6,
                'mixer_6': database.mixer_6,
                'v_comments_6': database.v_comments_6,
                'm_comments_6': database.m_comments_6,
            }
            if filled_in:
                empty_form = database
            else:
                empty_form = formL_form(initial=initial_data)
        else:
            this_week_saturday = ''
            week_almost = ''
            filled_in = False
            if new_saturday:
                set_start_date = today
                set_end_date = today + datetime.timedelta(days=6)
            elif new_sunday:
                set_start_date = sunday_last_sat
                set_end_date = today + datetime.timedelta(days=5)
            else:
                set_start_date = last_saturday
                set_end_date = end_week
            initial_data = {
                'week_start': set_start_date,
                'week_end': set_end_date
            }
            empty_form = formL_form(initial=initial_data)

        if request.method == "POST":
            if existing:
                form = formL_form(request.POST, instance=database)
            else:
                form = formL_form(request.POST)

            A_valid = form.is_valid()
            if A_valid:
                A = form.save()

                if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6}:
                    return redirect('../formH/formL')

                B = []
                print(last_saturday)
                
                for x in formL_model.objects.all():
                    if today_number not in {5,6}:
                        if x.week_start == last_saturday:
                            B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4))
                            B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3))
                            B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2))
                            B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1))
                            B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0))
                            B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6))
                            B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5))
                    else:
                        if x.week_start == todays_log.date_save - datetime.timedelta(days = (today_number - 5)):
                            B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4))
                            B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3))
                            B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2))
                            B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1))
                            B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0))
                            B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6))
                            B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5))

                for days in B:
                    if days[0] == today_number:
                        if days[1] and days[2] and days[3] and days[4] and days[5] and days[6]:
                            filled_in = True
                        else:
                            filled_in = False
                if filled_in:
                    done = Forms.objects.filter(form='L')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
                else:
                    done = Forms.objects.filter(form='L')[0]
                    done.submitted = False
                    done.date_submitted = todays_log.date_save - datetime.timedelta(days=1)
                    done.save()

                    return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formL.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'this_week_saturday': this_week_saturday, 'last_saturday': last_saturday, 'week_almost': week_almost, 'end_week': end_week, 'filled_in': filled_in, "access_page": access_page, 'profile': profile, 'opened': opened, 'formName': formName, 'admin': admin, "client": client, 'unlock': unlock
    })
