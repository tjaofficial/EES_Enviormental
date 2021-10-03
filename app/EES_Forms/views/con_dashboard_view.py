from django.shortcuts import render, redirect
import datetime
from django.contrib.auth.decorators import login_required
from ..models import user_profile_model, daily_battery_profile_model, Event, formA5_readings_model, formA5_model, formA1_readings_model, issues_model, formA4_model, User
import requests

lock = login_required(login_url='Login')
today = datetime.date.today()


@lock
def c_dashboard_view(request):
    if request.user.groups.filter(name='EES Coke Employees') or request.user.is_superuser or request.user.groups.filter(name='SGI Admin'):
        client = False
        if request.user.groups.filter(name='EES Coke Employees'):
            client = True

        today = datetime.date.today()
        profile = user_profile_model.objects.all()
        daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
        todays_log = daily_prof[0]

    # ----USER ON SCHEDULE----------

        event_cal = Event.objects.all()
        today = datetime.date.today()

        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer
            else:
                todays_obser = 'Schedule Not Updated'
    # ---90 DAY PUSH-------

        reads = formA5_readings_model.objects.all()
        # data = formA5_model.objects.all()

        def all_ovens(reads):
            A = []
            for items in reads:
                date = items.form.date
                # date_array = date.split("-")

                year = date.year
                month = date.month
                day = date.day

                form_date = datetime.datetime(year, month, day)
                added_date = form_date + datetime.timedelta(days=91)
                due_date = added_date - datetime.datetime.now()

                if len(str(items.o1)) == 1:
                    oven1 = "0" + str(items.o1)
                else:
                    oven1 = items.o1
                A.append((oven1, items.form.date, added_date.date, due_date.days))

                if len(str(items.o2)) == 1:
                    oven2 = "0" + str(items.o2)
                else:
                    oven2 = items.o2
                A.append((oven2, items.form.date, added_date.date, due_date.days))

                if len(str(items.o3)) == 1:
                    oven3 = "0" + str(items.o3)
                else:
                    oven3 = items.o3
                A.append((oven3, items.form.date, added_date.date, due_date.days))

                if len(str(items.o4)) == 1:
                    oven4 = "0" + str(items.o4)
                else:
                    oven4 = items.o4
                A.append((oven4, items.form.date, added_date.date, due_date.days))

            return A

        hello = all_ovens(reads)
        func = lambda x: (x[0], x[1])
        sort = sorted(hello, key=func, reverse=True)

        def final(sort):
            B = []
            i = 1
            for new in sort:
                B.append(new)

            for x in sort:
                for y in range(i, len(sort)):
                    tree = sort[y]
                    if tree[0] == x[0]:
                        if tree in B:
                            B.remove(tree)
                i += 1
            return B
        cool = final(sort)

        def overdue_30(cool):
            C = []
            for x in cool:
                if x[3] <= 30:
                    C.append(x)
            return C

        def overdue_10(cool):
            D = []
            for x in cool:
                if x[3] <= 10:
                    D.append(x)
            return D

        def overdue_5(cool):
            E = []
            for x in cool:
                if x[3] <= 5:
                    E.append(x)
            return E

        def overdue_closest(cool):
            F = []

            func2 = lambda R: (R[3])
            sort2 = sorted(cool, key=func2)
            most_recent = sort2[0][3]

            for x in sort2:
                if x[3] == most_recent:
                    F.append(x)
            return F

        od_30 = overdue_30(cool)
        od_10 = overdue_10(cool)
        od_5 = overdue_5(cool)
        od_recent = overdue_closest(cool)
    # ----WEATHER TAB-----------
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'

        city = 'Dearborn'

        city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'wind_speed': city_weather['wind']['speed'],
            'wind_direction': city_weather['wind']['deg'],
            'humidity': city_weather['main']['humidity'],
        }

        degree = weather['wind_direction']

        def toTextualDescription(degree):
            if degree > 337.5:
                return 'N'
            if degree > 292.5:
                return 'NW'
            if degree > 247.5:
                return 'W'
            if degree > 202.5:
                return 'SW'
            if degree > 157.5:
                return 'S'
            if degree > 122.5:
                return 'SE'
            if degree > 67.5:
                return 'E'
            if degree > 22.5:
                return 'NE'
            return 'N'

        wind_direction = toTextualDescription(degree)

    # ----ISSUES/CORRECTIVE ACTIONS----------

        ca_forms = issues_model.objects.all().order_by('-id')

    # ------------USERS-------------------

        Users = User.objects.all()
        profile = user_profile_model.objects.all()

    # ------FORM A-1 COLLECTION MAIN PRESURES---------

        formA1 = formA1_readings_model.objects.all().order_by('-form')
        recent_A1 = formA1[0]
        if str(today) == str(recent_A1):
            none_A1 = False
            charges = [('Charge #1', str(recent_A1.c1_sec) + ' sec'), ('Charge #2', str(recent_A1.c2_sec) + ' sec'), ('Charge #3', str(recent_A1.c3_sec) + ' sec'), ('Charge #4', str(recent_A1.c4_sec) + ' sec'), ('Charge #5', str(recent_A1.c5_sec) + ' sec'), ('Total Seconds', str(recent_A1.total_seconds) + ' sec')]
        else:
            none_A1 = True
            charges = [('Charge #1', 'N/A'), ('Charge #2', 'N/A'), ('Charge #3', 'N/A'), ('Charge #4', 'N/A'), ('Charge #5', 'N/A'), ('Total Seconds', 'N/A')]

    # ------FORM A-4 COLLECTION MAIN PRESURES---------

        formA4 = formA4_model.objects.all().order_by('-date')
        recent_A4 = formA4[0]
        if str(today) == str(recent_A4):
            none_A4 = False
            pressures = [('Main #1', recent_A4.main_1), ('Main #2', recent_A4.main_2), ('Main #3', recent_A4.main_3), ('Main #4', recent_A4.main_4), ('Suction Main', recent_A4.suction_main)]
        else:
            none_A4 = True
            pressures = [('Main #1', 'N/A'), ('Main #2', 'N/A'), ('Main #3', 'N/A'), ('Main #4', 'N/A'), ('Suction Main', 'N/A')]

    # -----PUSH TRAVELS--------------

        if len(str(today.month)) == 1:
            month = '0' + str(today.month)
        else:
            month = str(today.month)

        if len(str(today.day)) == 1:
            day = '0' + str(today.day)
        else:
            day = str(today.day)

        date_trans = str(today.year) + '-' + month + '-' + day

        org = formA5_model.objects.all().order_by('-date')
        database_form = org[0]
        org2 = formA5_readings_model.objects.all().order_by('-form')
        reads = org2[0]

        def double_digit(x):
            if len(x) == 1:
                double = '0' + x
                return double
            else:
                return x

        if str(todays_log.date_save) == str(database_form.date):
            ovens_reads = [{
                (reads.o1, 'p'): (
                    double_digit(reads.o1_1_reads),
                    double_digit(reads.o1_2_reads),
                    double_digit(reads.o1_3_reads),
                    double_digit(reads.o1_4_reads),
                    double_digit(reads.o1_5_reads),
                    double_digit(reads.o1_6_reads),
                    double_digit(reads.o1_7_reads),
                    double_digit(reads.o1_8_reads)
                ),
                (reads.o1, 't'): (
                     double_digit(reads.o1_9_reads),
                     double_digit(reads.o1_10_reads),
                     double_digit(reads.o1_11_reads),
                     double_digit(reads.o1_12_reads),
                     double_digit(reads.o1_13_reads),
                     double_digit(reads.o1_14_reads),
                     double_digit(reads.o1_15_reads),
                     double_digit(reads.o1_16_reads)
                )
            },
                {
                (reads.o2, 'p'): (
                    double_digit(reads.o2_1_reads),
                    double_digit(reads.o2_2_reads),
                    double_digit(reads.o2_3_reads),
                    double_digit(reads.o2_4_reads),
                    double_digit(reads.o2_5_reads),
                    double_digit(reads.o2_6_reads),
                    double_digit(reads.o2_7_reads),
                    double_digit(reads.o2_8_reads)),
                (reads.o2, 't'): (
                     double_digit(reads.o2_9_reads),
                     double_digit(reads.o2_10_reads),
                     double_digit(reads.o2_11_reads),
                     double_digit(reads.o2_12_reads),
                     double_digit(reads.o2_13_reads),
                     double_digit(reads.o2_14_reads),
                     double_digit(reads.o2_15_reads),
                     double_digit(reads.o2_16_reads)
                )
            },
                {
                (reads.o3, 'p'): (
                    double_digit(reads.o3_1_reads),
                    double_digit(reads.o3_2_reads),
                    double_digit(reads.o3_3_reads),
                    double_digit(reads.o3_4_reads),
                    double_digit(reads.o3_5_reads),
                    double_digit(reads.o3_6_reads),
                    double_digit(reads.o3_7_reads),
                    double_digit(reads.o3_8_reads)),
                (reads.o3, 't'): (
                     double_digit(reads.o3_9_reads),
                     double_digit(reads.o3_10_reads),
                     double_digit(reads.o3_11_reads),
                     double_digit(reads.o3_12_reads),
                     double_digit(reads.o3_13_reads),
                     double_digit(reads.o3_14_reads),
                     double_digit(reads.o3_15_reads),
                     double_digit(reads.o3_16_reads)
                )
            },
                {
                (reads.o4, 'p'): (
                    double_digit(reads.o4_1_reads),
                    double_digit(reads.o4_2_reads),
                    double_digit(reads.o4_3_reads),
                    double_digit(reads.o4_4_reads),
                    double_digit(reads.o4_5_reads),
                    double_digit(reads.o4_6_reads),
                    double_digit(reads.o4_7_reads),
                    double_digit(reads.o4_8_reads)),
                (reads.o4, 't'): (
                     double_digit(reads.o4_9_reads),
                     double_digit(reads.o4_10_reads),
                     double_digit(reads.o4_11_reads),
                     double_digit(reads.o4_12_reads),
                     double_digit(reads.o4_13_reads),
                     double_digit(reads.o4_14_reads),
                     double_digit(reads.o4_15_reads),
                     double_digit(reads.o4_16_reads)
                )
            },
            ]
            highest_p_list = [
                {'o1': max(ovens_reads[0][reads.o1, 'p'])},
                {'o2': max(ovens_reads[1][reads.o2, 'p'])},
                {'o3': max(ovens_reads[2][reads.o3, 'p'])},
                {'o4': max(ovens_reads[3][reads.o4, 'p'])},
            ]

            highest_t_list = [
                {'o1': max(ovens_reads[0][reads.o1, 't'])},
                {'o2': max(ovens_reads[1][reads.o2, 't'])},
                {'o3': max(ovens_reads[2][reads.o3, 't'])},
                {'o4': max(ovens_reads[3][reads.o4, 't'])},
            ]

            highest_push = highest_p_list[0]['o1']
            highest_travel = highest_t_list[0]['o1']

            high_push = highest_push + "%"
            high_travel = highest_travel + '%'

            none_A5 = False
        else:
            none_A5 = True
            high_push = 'N/A'
            high_travel = 'N/A'

    else:
        return redirect('IncompleteForms')

    return render(request, 'ees_forms/c_dashboard.html', {
        'profile': profile, 'high_push': high_push, 'high_travel': high_travel, 'todays_log': todays_log, 'todays_obser': todays_obser, 'od_30': od_30, 'weather': weather, "today": date_trans, 'ca_forms': ca_forms, 'wind_direction': wind_direction, 'Users': Users, 'client': client, 'pressures': pressures, 'charges': charges, 'none_A1': none_A1, "none_A4": none_A1, 'none_A5': none_A5
    })
