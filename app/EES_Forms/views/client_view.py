from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import issues_model, formA1_readings_model, formA2_model, formA3_model, Event, formA4_model, formA5_readings_model, daily_battery_profile_model, Forms, User, user_profile_model, bat_info_model
import datetime
import json
import requests
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import setUnlockClientSupervisor, weatherDict, calculateProgessBar, getCompanyFacilities

lock = login_required(login_url='Login')

@lock
def client_dashboard_view(request, facility):
    options = bat_info_model.objects.all()
    supervisor = False
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('facilitySelect')
    if supervisor:
        return redirect('sup_dashboard', SUPER_VAR)
    formA1 = formA1_readings_model.objects.all().order_by('-form')
    formA2 = formA2_model.objects.all().order_by('-date')
    formA3 = formA3_model.objects.all().order_by('-date')
    formA4 = formA4_model.objects.all().order_by('-date')
    formA5 = formA5_readings_model.objects.all().order_by('-form')
    reads = formA5_readings_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    now = datetime.datetime.now().date()
    options = bat_info_model.objects.filter(facility_name=facility)
    emypty_dp_today = True
    userProfile = user_profile_model.objects.get(user__id=request.user.id)
    userCompany = userProfile.company
    if options.exists():
        options = options[0]
    #VVV i may not need this because the facility is perminent for the client VVV
    if facility != CLIENT_VAR:
        recent_logs = formA1_readings_model.objects.all().filter(form__facilityChoice__facility_name=facility).order_by('-form')[:7]
    else:
        recent_logs = ''
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
    if facility != 'supervisor':
        daily_percent = calculateProgessBar(facility, 'Daily')
        weekly_percent = calculateProgessBar(facility, "Weekly")
        monthly_percent = calculateProgessBar(facility, 'Monthly')
        quarterly_percent = calculateProgessBar(facility, 'Quarterly')
        annually_percent = 0
    else:
        daily_percent = ''
        weekly_percent = ''
        monthly_percent = ''
        quarterly_percent = ''
        annually_percent = ''
    # -------90 DAY PUSH ----------------

    def all_ovens(reads):
        A = []
        for items in reads:
            if items.form.facilityChoice == facility:
                date = items.form.date

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
    if hello:
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
        if len(cool) >= 4:
            od_30 = overdue_30(cool)
            od_10 = overdue_10(cool)
            od_5 = overdue_5(cool)
            od_recent = overdue_closest(cool)
        else:
            od_recent = ''
            od_30 = ''
            od_10 = ''
            od_5 = ''
    else:
        od_recent = ''
        od_10 = ''
        od_5 = ''
        od_30 = ''

    # ----CONTACTS-----------------
    allContacts = user_profile_model.objects.filter(company=userCompany)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    # ----USER ON SCHEDULE----------
    todays_obser = 'Schedule Not Updated'
    event_cal = Event.objects.all()
    today = datetime.date.today()

    if len(event_cal) > 0:
        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer

    # ----ISSUES/CORRECTIVE ACTIONS----------

    ca_forms = issues_model.objects.all().filter(facilityChoice__facility_name=facility).order_by('-id')

    # ----WEATHER TAB-----------
    # Weather API Pull
    if facility == 'supervisor':
        weather = weatherDict(False)
    else:
        weather = weatherDict(options.city)
    # ----OTHER-----------    
    if request.user.groups.filter(name=CLIENT_VAR) or request.user.is_superuser:
        if daily_prof.exists():
            todays_log = daily_prof[0]
            if now == todays_log.date_save:
                emypty_dp_today = False
                today = todays_log.date_save
                if len(formA1) > 0:
                    newA1 = formA1.filter(form__facilityChoice__facility_name=facility).order_by('-form')
                    if len(newA1) > 0:
                        most_recent_A1 = newA1[0].form.date
                    else:
                        most_recent_A1 = ''
                    if most_recent_A1 == today:
                        A1data = formA1[0]
                        form_enteredA1 = True
                    else:
                        A1data = ""
                else:
                    A1data = ""

                if len(formA2) > 0:
                    newA2 = formA2.filter(facilityChoice__facility_name=facility).order_by('-date')
                    if len(newA2) > 0:
                        most_recent_A2 = newA2[0].date
                    else:
                        most_recent_A2 = ''
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
                    newA3 = formA3.filter(facilityChoice__facility_name=facility).order_by('-date')
                    if len(newA3) > 0:
                        most_recent_A3 = formA3[0].date
                    else:
                        most_recent_A3 = ''
                    if most_recent_A3 == today:
                        A3data = formA3[0]
                        if A3data.l_leak_json and A3data.om_leak_json:
                            lids = json.loads(A3data.l_leak_json)
                            offtakes = json.loads(A3data.om_leak_json)
                        else:
                            lids = ""
                            offtakes = ""
                        form_enteredA3 = True
                    else:
                        A3data = ""
                        lids = ""
                        offtakes = ""
                else:
                    print('CHECK 2')
                    A3data = ""
                    lids = ""
                    offtakes = ""

                if len(formA4) > 0:
                    newA4 = formA4.filter(facilityChoice__facility_name=facility).order_by('-date')
                    if len(newA4) > 0:
                        most_recent_A4 = formA4[0].date
                    else:
                        most_recent_A4 = ''
                    if most_recent_A4 == today:
                        A4data = formA4[0]
                        form_enteredA4 = True
                    else:
                        A4data = ""
                else:
                    A4data = ""

                if len(formA5) > 0:
                    newA5 = formA5.filter(form__facilityChoice__facility_name=facility).order_by('-form')
                    if len(newA5) > 0:
                        most_recent_A5 = formA5[0].form.date
                    else:
                        most_recent_A5 = ''
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
            if request.method == 'POST':
                answer = request.POST
                if answer['facilitySelect'] != '':
                    return redirect('sup_dashboard', answer['facilitySelect'])
            return render(request, "supervisor/sup_dashboard.html", {
                'facility': facility, 
                'ca_forms': ca_forms, 
                'recent_logs': recent_logs, 
                'todays_obser': todays_obser, 
                'profile': allContacts, 
                'weather': weather, 
                'od_recent': od_recent, 
                'weekly_percent': weekly_percent, 
                'monthly_percent': monthly_percent, 
                'annually_percent': annually_percent, 
                'daily_percent': daily_percent, 
                'supervisor': supervisor,  
                "client": client, 
                'unlock': unlock,
                'sortedFacilityData': sortedFacilityData,
            })
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard', answer['facilitySelect'])
        
    return render(request, "supervisor/sup_dashboard.html", {
        'facility': facility, 
        'form_enteredA5': form_enteredA5, 
        'form_enteredA4': form_enteredA4, 
        'form_enteredA3': form_enteredA3, 
        'form_enteredA2': form_enteredA2,
        'form_enteredA1': form_enteredA1, 
        'date': date, 
        "od_10": od_10, 
        "od_5": od_5, 
        "od_30": od_30, 
        'recent_logs': recent_logs, 
        'lids': lids, 
        'offtakes': offtakes, 
        'ca_forms': ca_forms, 
        'weather': weather, 
        'todays_log': todays_log, 
        'todays_obser': todays_obser, 
        'profile': allContacts, 
        'A1data': A1data, 
        'A2data': A2data, 
        'A3data': A3data, 
        'A4data': A4data, 
        'A5data': A5data, 
        'push': push, 
        'coke': coke, 
        'od_recent': od_recent, 
        'weekly_percent': weekly_percent, 
        'monthly_percent': monthly_percent, 
        'annually_percent': annually_percent, 
        'daily_percent': daily_percent,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'sortedFacilityData': sortedFacilityData, 
    })
