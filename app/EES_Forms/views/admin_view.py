from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import CreateUserForm, user_profile_form
from ..models import issues_model, formA1_readings_model, formA2_model, formA3_model, Event, formA4_model, formA5_readings_model, daily_battery_profile_model, Forms, User, user_profile_model
import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
import json
import requests

lock = login_required(login_url='Login')


def admin_dashboard_view(request):
    formA1 = formA1_readings_model.objects.all().order_by('-form')
    formA2 = formA2_model.objects.all().order_by('-date')
    formA3 = formA3_model.objects.all().order_by('-date')
    formA4 = formA4_model.objects.all().order_by('-date')
    formA5 = formA5_readings_model.objects.all().order_by('-form')
    reads = formA5_readings_model.objects.all()
    count_bp = daily_battery_profile_model.objects.count()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    emypty_dp_today = True
    recent_logs = formA1_readings_model.objects.all().order_by('-form')[:7]

    # -------PROGRESS PERCENTAGES -----------------

    weekly_forms_total = []
    weekly_forms_comp = []
    for forms in Forms.objects.all():
        if forms.frequency in {"Daily", "Weekly"}:
            weekly_forms_total.append(forms.form)
            if forms.submitted:
                weekly_forms_comp.append(forms.form)
    weekly_count_total = len(weekly_forms_total)
    weekly_count_comp = len(weekly_forms_comp)
    weekly_percent = (weekly_count_comp / weekly_count_total) * 100

    monthly_forms_total = []
    monthly_forms_comp = []
    for forms in Forms.objects.all():
        if forms.frequency in {"Monthly"}:
            monthly_forms_total.append(forms.form)
            if forms.submitted:
                weekly_forms_comp.append(forms.form)
    monthly_count_total = len(monthly_forms_total)
    monthly_count_comp = len(monthly_forms_comp)
    monthly_percent = (monthly_count_comp / monthly_count_total) * 100

    annually_forms_total = [1]
    annually_forms_comp = []
    for forms in Forms.objects.all():
        if forms.frequency in {"Annually"}:
            annually_forms_total.append(forms.form)
            if forms.submitted:
                weekly_forms_comp.append(forms.form)
    annually_count_total = len(annually_forms_total)
    annually_count_comp = len(annually_forms_comp)
    annually_percent = (annually_count_comp / annually_count_total) * 100

    # -------90 DAY PUSH ----------------

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

    # ----CONTACTS-----------------

    Users = User.objects.all()
    profile = user_profile_model.objects.all()

    # ----USER ON SCHEDULE----------

    event_cal = Event.objects.all()
    today = datetime.date.today()

    if len(event_cal) > 0:
        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer
            else:
                todays_obser = 'Schedule Not Updated'
    else:
        todays_obser = 'Schedule Not Updated'

    # ----ISSUES/CORRECTIVE ACTIONS----------

    ca_forms = issues_model.objects.all().order_by('-id')

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

    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        if count_bp != 0:
            todays_log = daily_prof[0]
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    print('check 1')
                    emypty_dp_today = False
                    today = todays_log.date_save
                    if len(formA1) > 0:
                        most_recent_A1 = formA1[0].form.date
                        if most_recent_A1 == today:
                            A1data = formA1[0]
                        else:
                            A1data = ""
                    else:
                        A1data = ""

                    if len(formA2) > 0:
                        most_recent_A2 = formA2[0].date
                        if most_recent_A2 == today:
                            A2data = formA2[0]
                            push = json.loads(A2data.p_leak_data)
                            coke = json.loads(A2data.c_leak_data)
                        else:
                            A2data = ""
                            push = ""
                            coke = ""
                    else:
                        A2data = ""
                        push = ""
                        coke = ""

                    if len(formA3) > 0:
                        most_recent_A3 = formA3[0].date
                        if most_recent_A3 == today:
                            A3data = formA3[0]
                            lids = json.loads(A3data.l_leak_json)
                            offtakes = json.loads(A3data.om_leak_json)
                        else:
                            A3data = ""
                            lids = ""
                            offtakes = ""
                    else:
                        A3data = ""
                        lids = ""
                        offtakes = ""

                    if len(formA4) > 0:
                        most_recent_A4 = formA4[0].date
                        if most_recent_A4 == today:
                            A4data = formA4[0]
                        else:
                            A4data = ""
                    else:
                        A4data = ""

                    if len(formA5) > 0:
                        most_recent_A5 = formA5[0].form.date
                        if most_recent_A5 == today:
                            A5data = formA5[0]
                            print('water')
                        else:
                            A5data = ""
                    else:
                        A5data = ""
        else:
            formA4 = ""
            todays_log = ''

        if emypty_dp_today:
            return render(request, "admin/admin_dashboard.html", {
                'ca_forms': ca_forms, 'recent_logs': recent_logs, 'todays_obser': todays_obser, 'Users': Users, 'profile': profile, 'weather': weather, 'wind_direction': wind_direction, 'od_recent': od_recent, 'weekly_percent': weekly_percent, 'monthly_percent': monthly_percent, 'annually_percent': annually_percent
            })
    return render(request, "admin/admin_dashboard.html", {
        'recent_logs': recent_logs, 'lids': lids, 'offtakes': offtakes, 'ca_forms': ca_forms, 'weather': weather, 'wind_direction': wind_direction, 'todays_log': todays_log, 'todays_obser': todays_obser, 'Users': Users, 'profile': profile, 'A1data': A1data, 'A2data': A2data, 'A3data': A3data, 'A4data': A4data, 'A5data': A5data, 'push': push, 'coke': coke, 'od_recent': od_recent, 'weekly_percent': weekly_percent, 'monthly_percent': monthly_percent, 'annually_percent': annually_percent
    })


def register_view(request):
    # change code to redirect if you are not roger/SGI ADMIN
    if not request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        return redirect('IncompleteForms')
    else:
        form = CreateUserForm()
        profile_form = user_profile_form()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = user_profile_form(request.POST)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                profile.save()

                group = Group.objects.get(name=profile.position)
                user.groups.add(group)

                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "The Information Entered Was Invalid.")
    return render(request, "ees_forms/ees_register.html", {
                'form': form, 'profile_form': profile_form
            })
