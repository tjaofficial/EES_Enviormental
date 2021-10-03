from django.shortcuts import render, redirect
from ..models import user_profile_model, formA5_readings_model, Forms, daily_battery_profile_model
from django.contrib.auth.decorators import login_required
import datetime
import requests
from django.contrib.auth.models import User

lock = login_required(login_url='Login')
now = datetime.datetime.now()


@lock
def IncompleteForms(request):
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser or request.user.groups.filter(name='SGI Quality Control'):
        profile = user_profile_model.objects.all()
        today = datetime.date.today()
        todays_num = today.weekday()
        sub_forms = Forms.objects.all()
        reads = formA5_readings_model.objects.all()
        today_str = str(today)

        weekday_fri = today + datetime.timedelta(days=4 - todays_num)
        weekend_fri = weekday_fri + datetime.timedelta(days=7)

    # ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
    # ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
        if Forms.objects.count() <= 5:
            A1 = Forms(
                form="A-1",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formA1",
                header="Method 303",
                title="Charging",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            A2 = Forms(
                form="A-2",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formA2",
                header="Method 303",
                title="Doors",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            A3 = Forms(
                form="A-3",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formA3",
                header="Method 303",
                title="Lids and Offtakes",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            A4 = Forms(
                form="A-4",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formA4",
                header="Method 303",
                title="Collection Main",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            A5 = Forms(
                form="A-5",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formA5",
                header="Method 9B",
                title="Push Travels",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            B = Forms(
                form="B",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=True,
                weekend_only=False,
                link="formB",
                header="Method 9",
                title="Fugitive Dust Inspection",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            C = Forms(
                form="C",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formC",
                header="Method 9",
                title="Method 9D - Coal Field",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            D = Forms(
                form="D",
                frequency="Weekly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formD",
                header="Method 9",
                title="Random Truck Inspection",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            E = Forms(
                form="E",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formE",
                header="Method 9",
                title="Gooseneck Inspection",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            F1 = Forms(
                form="F-1",
                frequency="Weekly",
                day_freq='Wednesday',
                weekdays_only=False,
                weekend_only=False,
                link="formF1",
                header="Waste Weekly Inspections",
                title="SIF / K087 Process Area (Satellite)",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            F2 = Forms(
                form="F-2",
                frequency="Weekly",
                day_freq='Wednesday',
                weekdays_only=False,
                weekend_only=False,
                link="formF2",
                header="Waste Weekly Inspections",
                title="#1 Shop (Satellite Accumulation)",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            F3 = Forms(
                form="F-3",
                frequency="Weekly",
                day_freq='Wednesday',
                weekdays_only=False,
                weekend_only=False,
                link="formF3",
                header="Waste Weekly Inspections",
                title="#2 Shop (Satellite Accumulation)",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            F4 = Forms(
                form="F-4",
                frequency="Weekly",
                day_freq='Wednesday',
                weekdays_only=False,
                weekend_only=False,
                link="formF4",
                header="Waste Weekly Inspections",
                title="Battery (Satellite Accumulation)",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            F5 = Forms(
                form="F-5",
                frequency="Weekly",
                day_freq='Wednesday',
                weekdays_only=False,
                weekend_only=False,
                link="formF5",
                header="Waste Weekly Inspections",
                title="Bio Plant (Satellite Accumulation)",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            F6 = Forms(
                form="F-6",
                frequency="Weekly",
                day_freq='Wednesday',
                weekdays_only=False,
                weekend_only=False,
                link="formF6",
                header="Waste Weekly Inspections",
                title="No. 8 Tank Area (Satellite Accumulation)",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            F7 = Forms(
                form="F-7",
                frequency="Weekly",
                day_freq='Wednesday',
                weekdays_only=False,
                weekend_only=False,
                link="formF7",
                header="Waste Weekly Inspections",
                title="Booster Pad (90-Day Accumulation)",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            G1 = Forms(
                form="G-1",
                frequency="Weekly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formG1",
                header="PECS Baghouse Stack",
                title="Method 9/Non-Certified Observations",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            G2 = Forms(
                form="G-2",
                frequency="Weekly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formG2",
                header="PECS Baghouse Stack",
                title="Method 9B",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            H = Forms(
                form="H",
                frequency="Weekly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formH",
                header="Method 9",
                title="Method 9 - Combustion Stack",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            I = Forms(
                form="I",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=True,
                weekend_only=False,
                link="formI",
                header="Sampling",
                title="Quench Water Sampling Form",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            L = Forms(
                form="L",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formL",
                header="Method 9",
                title="Visual Emissions Observations",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            M = Forms(
                form="M",
                frequency="Daily",
                day_freq='Any',
                weekdays_only=True,
                weekend_only=False,
                link="formM",
                header="Method 9D",
                title="Method 9D Observation",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            N = Forms(
                form="N",
                frequency="Monthly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="formN",
                header="Fugitive Dust Inspection",
                title="Method 9D Monthly Checklist",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            O = Forms(
                form="O",
                frequency="Weekly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=True,
                link="formO",
                header="Stormwater Observation Form",
                title="MP 108A",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            P = Forms(
                form="P",
                frequency="Weekly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=True,
                link="formP",
                header="Outfall Observation Form",
                title="Outfall 008",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)
            spill_kits = Forms(
                form="Spill Kits",
                frequency="Monthly",
                day_freq='Any',
                weekdays_only=False,
                weekend_only=False,
                link="spill_kits",
                header="Spill Kits Form",
                title="Inspection Check List",
                due_date=today,
                date_submitted=today - datetime.timedelta(days=1),
                submitted=False,)

            A1.save()
            A2.save()
            A3.save()
            A4.save()
            A5.save()
            B.save()
            C.save()
            D.save()
            E.save()
            F1.save()
            F2.save()
            F3.save()
            F4.save()
            F5.save()
            F6.save()
            F7.save()
            G1.save()
            G2.save()
            H.save()
            I.save()
            L.save()
            M.save()
            N.save()
            O.save()
            P.save()
            spill_kits.save()

    # --------------------------------------------Closest Oven Due-----------------
    # --------------------------------------------Closest Oven Due-----------------
    # --------------------------------------------Closest Oven Due-----------------

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

        def overdue_closest(cool):
            F = []

            func2 = lambda R: (R[3])
            sort2 = sorted(cool, key=func2)
            most_recent = sort2[0][3]

            for x in sort2:
                if x[3] == most_recent:
                    F.append(x)
            return F

        if len(cool) >= 4:
            od_recent = overdue_closest(cool)
        else:
            od_recent = ''


    # --------------------------------------------Battery Profile Data------------
    # --------------------------------------------Battery Profile Data------------
    # --------------------------------------------Battery Profile Data------------
        daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
        todays_log = daily_prof[0]

        profile_entered = False
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                profile_entered = True

    # ------------------------------------------------------Weather-------------
    # ------------------------------------------------------Weather-------------
    # ------------------------------------------------------Weather-------------

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

    # ------------------------------------------------------Form Data-------------
        for forms in sub_forms:
            if todays_num in {0, 1, 2, 3, 4}:
                forms.due_date = weekday_fri

                A = forms.date_submitted
                if today != A:
                    forms.submitted = False
                    forms.save()
            else:
                forms.due_date = weekend_fri

                A = forms.date_submitted
                if today != A:
                    forms.submitted = False
                    forms.save()

        pull = Forms.objects.filter(submitted__exact=False).order_by('form')
        pullNot = Forms.objects.filter(submitted__exact=True).order_by('form')

        day_number = today.weekday()

        if day_number == 6:
            saturday = False
        else:
            saturday = True

        weekend_list = [5, 6]
        form_check1 = ["", ]
        form_check2 = ["", ]

    else:
        poop = User.objects.all().order_by('id')
        print(poop[1].groups.all())
        for a in poop:
            print(a)
            print(a.groups.all())
            print('')
            q_group = a.groups.all()
            for x in q_group:
                print(x)
                if str(x) == 'EES Coke Employees':
                    print(a)
                    print(x)
                    return redirect('c_dashboard')

    return render(request, "ees_forms/dashboard.html", {
        "pull": pull, "pullNot": pullNot, "today": today, 'od_recent': od_recent, "todays_log": todays_log, 'now': now, 'profile_entered': profile_entered, 'form_check1': form_check1, 'form_check2': form_check2, 'profile': profile, 'today_str': today_str, 'todays_num': todays_num, 'day_number': day_number, 'weekend_list': weekend_list, 'weather': weather, 'wind_direction': wind_direction, 'saturday': saturday,
    })
