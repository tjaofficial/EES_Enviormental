from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import issues_model, formA1_readings_model, formA2_model, formA3_model, Event, formA4_model, formA5_readings_model, daily_battery_profile_model, Forms, User, user_profile_model
import datetime
import json
import requests

lock = login_required(login_url='Login')

@lock
def client_dashboard_view(request):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    formA1 = formA1_readings_model.objects.all().order_by('-form')
    formA2 = formA2_model.objects.all().order_by('-date')
    formA3 = formA3_model.objects.all().order_by('-date')
    formA4 = formA4_model.objects.all().order_by('-date')
    formA5 = formA5_readings_model.objects.all().order_by('-form')
    all_db_reads = formA5_readings_model.objects.all()
    count_bp = daily_battery_profile_model.objects.count()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    
    emypty_dp_today = True
    recent_logs = formA1_readings_model.objects.all().order_by('-form')[:7]
    now = datetime.datetime.now()
    year = str(now.year)
    if len(str(now.month)) == 1:
        month = "0" + str(now.month)
    else:
        month = str(now.month)
    if len(str(now.day)) == 1:
        day = '0' + str(now.day)
    else:
        day = str(now.day)
    date = year + '-' + month + '-' + day
    form_enteredA1 = False
    form_enteredA2 = False
    form_enteredA3 = False
    form_enteredA4 = False
    form_enteredA5 = False
    today = datetime.date.today()
    todays_num = today.weekday()
    # -------PROGRESS PERCENTAGES -----------------

    daily_forms_comp = []
    for forms in Forms.objects.filter(frequency = 'Daily'):
        if forms.submitted:
            daily_forms_comp.append(forms.form)
    if todays_num in {0, 1, 2, 3, 4}:
        daily_count_total = 11
    else:
        daily_count_total = 8
    daily_count_comp = len(daily_forms_comp)
    daily_percent = (daily_count_comp / daily_count_total) * 100

    weekly_forms_comp = []
    for forms in Forms.objects.all():
        if forms.frequency in {"Daily", "Weekly"}:
            if forms.submitted:
                weekly_forms_comp.append(forms.form)
    weekly_count_total = 60
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
        for p in reads:
            date = p.form.date
            list = [p.o1, p.o2, p.o3, p.o4]
            year = date.year
            month = date.month
            day = date.day

            dateAdded = datetime.datetime(year, month, day)
            EXPdate = dateAdded + datetime.timedelta(days=91)
            daysLeft = EXPdate - datetime.datetime.now()
            
            for q in list:
                if len(str(q)) == 1:
                    ovenNumber = "0" + str(q)
                else:
                    ovenNumber = q

                A.append((ovenNumber, p.form.date, EXPdate.date, daysLeft.days))
        return A
    all_read_ovens = all_ovens(all_db_reads)
    func = lambda x: (x[0], x[1])
    sort_by_oven = sorted(all_read_ovens, key=func, reverse=True)
    
    print('START HERE')
    
    def final(organizedOvens):
        B = []
        i = 1
        for oven_a in organizedOvens:
            B.append(oven_a)
        for oven_b in organizedOvens:
            for y in range(i, len(organizedOvens)):
                check_instance = organizedOvens[y]
                if check_instance[0] == oven_b[0]:
                    if check_instance in B:
                        B.remove(check_instance)
            i += 1

        for n in range(1, 86):
            for oven in B:
                if len(str(n)) == 1:
                    zero_n = "0" + str(n)
                else:
                    zero_n = str(n)
                    
                if zero_n == oven[0]:
                    exist = True
                    break
                else:
                    exist = False
            if not exist:
                B.append((zero_n, 'N/A', 0, 0))              
        return B
    all_ovens_EXP = final(sort_by_oven)
    
    def sort_key(oven):
        return oven[0]
    all_ovens_EXP.sort(key=sort_key, reverse=True) 
    
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
    if len(all_ovens_EXP) >= 4:
        od_30 = overdue_30(all_ovens_EXP)
        od_10 = overdue_10(all_ovens_EXP)
        od_5 = overdue_5(all_ovens_EXP)
        od_recent = overdue_closest(all_ovens_EXP)
    else:
        od_recent = ''
        od_30 = ''
        od_10 = ''
        od_5 = ''

    # ----CONTACTS-----------------

    Users = User.objects.all()
    profile = user_profile_model.objects.all()

    # ----USER ON SCHEDULE----------
    todays_obser = 'Schedule Not Updated'

    event_cal = Event.objects.all()
    today = datetime.date.today()

    if len(event_cal) > 0:
        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer

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

    if request.user.groups.filter(name='EES Coke Employees') or request.user.is_superuser:
        if count_bp != 0:
            todays_log = daily_prof[0]
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    emypty_dp_today = False
                    today = todays_log.date_save
                    if len(formA1) > 0:
                        most_recent_A1 = formA1[0].form.date
                        if most_recent_A1 == today:
                            A1data = formA1[0]
                            form_enteredA1 = True
                        else:
                            A1data = ""
                    else:
                        A1data = ""

                    if len(formA2) > 0:
                        most_recent_A2 = formA2[0].date
                        if most_recent_A2 == today:
                            A2data = formA2[0]
                            if A2data.p_leak_data and A2data.c_leak_data:
                                push = json.loads(A2data.p_leak_data)
                                coke = json.loads(A2data.c_leak_data)
                            else:
                                push = ""
                                coke = ""
                            form_enteredA2 = True
                        else:
                            A2data = ""
                            push = ""
                            coke = ""
                    else:
                        A2data = ""
                        push = ""
                        coke = ""

                    if len(formA3) > 0:
                        print('CHECK 1')
                        most_recent_A3 = formA3[0].date
                        if most_recent_A3 == today:
                            print('CHECK 1.1')
                            A3data = formA3[0]
                            if A3data.l_leak_json and A3data.om_leak_json:
                                print('CHECK 1.1.1')
                                lids = json.loads(A3data.l_leak_json)
                                offtakes = json.loads(A3data.om_leak_json)
                            else:
                                print('CHECK 1.1.2')
                                lids = ""
                                offtakes = ""
                            form_enteredA3 = True
                        else:
                            print('CHECK 1.2')
                            A3data = ""
                            lids = ""
                            offtakes = ""
                    else:
                        print('CHECK 2')
                        A3data = ""
                        lids = ""
                        offtakes = ""

                    if len(formA4) > 0:
                        most_recent_A4 = formA4[0].date
                        if most_recent_A4 == today:
                            A4data = formA4[0]
                            form_enteredA4 = True
                        else:
                            A4data = ""
                    else:
                        A4data = ""

                    if len(formA5) > 0:
                        most_recent_A5 = formA5[0].form.date
                        if most_recent_A5 == today:
                            A5data = formA5[0]
                            form_enteredA5 = True
                        else:
                            A5data = ""
                    else:
                        A5data = ""
        else:
            formA4 = ""
            todays_log = ''

        if emypty_dp_today:
            return render(request, "client/client_dashboard.html", {
                'ca_forms': ca_forms, 'recent_logs': recent_logs, 'todays_obser': todays_obser, 'Users': Users, 'profile': profile, 'weather': weather, 'wind_direction': wind_direction, 'od_recent': od_recent, 'weekly_percent': weekly_percent, 'monthly_percent': monthly_percent, 'annually_percent': annually_percent, 'daily_percent': daily_percent,
            })
    return render(request, "client/client_dashboard.html", {
        'admin': admin, "client": client, 'unlock': unlock, 'form_enteredA5': form_enteredA5, 'form_enteredA4': form_enteredA4, 'form_enteredA3': form_enteredA3, 'form_enteredA2': form_enteredA2,'form_enteredA1': form_enteredA1, 'date': date, "od_10": od_10, "od_5": od_5, "od_30": od_30, 'recent_logs': recent_logs, 'lids': lids, 'offtakes': offtakes, 'ca_forms': ca_forms, 'weather': weather, 'wind_direction': wind_direction, 'todays_log': todays_log, 'todays_obser': todays_obser, 'Users': Users, 'profile': profile, 'A1data': A1data, 'A2data': A2data, 'A3data': A3data, 'A4data': A4data, 'A5data': A5data, 'push': push, 'coke': coke, 'od_recent': od_recent, 'weekly_percent': weekly_percent, 'monthly_percent': monthly_percent, 'annually_percent': annually_percent, 'daily_percent': daily_percent,
    })
