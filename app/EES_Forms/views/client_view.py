from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import issues_model, form1_readings_model, form2_model, form3_model, Event, form4_model, form5_readings_model, daily_battery_profile_model, form1_readings_model, User, user_profile_model, bat_info_model
import datetime
import json
import requests
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import setUnlockClientSupervisor2, weatherDict, calculateProgessBar, getCompanyFacilities,checkIfFacilitySelected, userGroupRedirect, tryExceptFormDatabases,updateAllFormSubmissions, ninetyDayPushTravels

lock = login_required(login_url='Login')

@lock
def client_dashboard_view(request, facility):
    permissions = [CLIENT_VAR]
    userGroupRedirect(request.user, permissions)
    updateAllFormSubmissions(facility)
    notifs = checkIfFacilitySelected(request.user, facility)
    options = bat_info_model.objects.all()
    supervisor = False
    unlock, client, supervisor = setUnlockClientSupervisor2(request.user)
    formA1 = form1_readings_model.objects.all().order_by('-form')
    formA2 = form2_model.objects.all().order_by('-date')
    formA3 = form3_model.objects.all().order_by('-date')
    formA4 = form4_model.objects.all().order_by('-date')
    formA5 = form5_readings_model.objects.all().order_by('-form')
    fsID1 = tryExceptFormDatabases(1,formA1, facility)
    fsID2 = tryExceptFormDatabases(2,formA2, facility) 
    fsID3 = tryExceptFormDatabases(3,formA3, facility)
    fsID4 = tryExceptFormDatabases(4,formA4, facility)
    fsID5 = tryExceptFormDatabases(5,formA5, facility)
    fsIDs = [fsID1,fsID2,fsID3,fsID4,fsID5]
    print(fsIDs)
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    now = datetime.datetime.now().date()
    last7days = now - datetime.timedelta(days=6)
    options = bat_info_model.objects.filter(facility_name=facility)
    emypty_dp_today = True
    userProfile = user_profile_model.objects.get(user__id=request.user.id)
    userCompany = userProfile.company
    if options.exists():
        options = options[0]
    #VVV i may not need this because the facility is perminent for the client VVV
    if facility != CLIENT_VAR:
        recent_logs = form1_readings_model.objects.all().filter(form__facilityChoice__facility_name=facility).order_by('-form')[:7]
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
    
    #---------- Graph Data ---------------------
    dateList = []
    dateListD = []
    dateListL = []
    top7xValues = []
    top7yValues = []
    top7Query = formA1[:7]
    for x in range(0,6):
        if today + datetime.timedelta(days=x) not in dateList:
            dateList.append(today - datetime.timedelta(days=x))
            dateListD.append(today - datetime.timedelta(days=x))
            dateListL.append(today - datetime.timedelta(days=x))
    for dates in dateList:
        for chargeEntry in top7Query:
            if chargeEntry.form.date == dates:
                top7xValues.append(int(chargeEntry.total_seconds))
                top7yValues.append(str(chargeEntry.form.date))
                break
        if str(dates) not in top7yValues:
            top7xValues.append(int(0))
            top7yValues.append(str(dates))
    top7yValues = json.dumps(top7yValues)

    top7xValuesD = []
    top7yValuesD = []
    top7QueryD = formA2[:7]
    for dates in dateList:
        for doorEntry in top7QueryD:
            if doorEntry.date == dates:
                top7xValuesD.append(int(doorEntry.leaking_doors))
                top7yValuesD.append(str(doorEntry.date))
                break
        if str(dates) not in top7yValuesD:
            top7xValuesD.append(int(0))
            top7yValuesD.append(str(dates))
    top7yValuesD = json.dumps(top7yValuesD)
        
    top7xValuesL = []
    top7yValuesL = []
    top7QueryL = formA3[:7]
    for dates in dateList:
        for lidEntry in top7QueryL:
            if lidEntry.date == dates:
                top7xValuesL.append(int(lidEntry.l_leaks))
                top7yValuesL.append(str(lidEntry.date))
                break
        if str(dates) not in top7yValuesL:
            top7xValuesL.append(int(0))
            top7yValuesL.append(str(dates))
    top7yValuesL = json.dumps(top7yValuesL)
    
    # -------PROGRESS PERCENTAGES -----------------
    if facility != 'supervisor':
        daily_percent = calculateProgessBar(facility, 'Daily')
        weekly_percent = calculateProgessBar(facility, "Weekly")
        monthly_percent = calculateProgessBar(facility, 'Monthly')
        quarterly_percent = calculateProgessBar(facility, 'Quarterly')
        annually_percent = 0
    else:
        daily_percent = False
        weekly_percent = False
        monthly_percent = False
        quarterly_percent = False
        annually_percent = False
    # -------90 DAY PUSH ----------------
    pushTravelsData = ninetyDayPushTravels(facility)
    if pushTravelsData == 'EMPTY':
        od_30 = ''
        od_10 = ''
        od_5 = ''
        od_recent = ''
        all_ovens = ''
    else:
        od_30 = pushTravelsData['30days']
        od_10 = pushTravelsData['10days']
        od_5 = pushTravelsData['5days']
        od_recent = pushTravelsData['closest']
        all_ovens = pushTravelsData['all']
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
    # ----Weather API Pull-----------
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
                if formA1.exists():
                    most_recent_A1 = formA1[0].form.date
                    if most_recent_A1 == today:
                        A1data = formA1[0]
                        form_enteredA1 = True
                    else:
                        A1data = ""
                else:
                    A1data = ""

                A2data = ""
                push = ""
                coke = ""
                pLeaks = 0
                cLeaks = 0
                if formA2.exists():
                    most_recent_A2 = formA2[0]
                    if most_recent_A2.date == today:
                        A2data = most_recent_A2
                        if most_recent_A2.p_leak_data and most_recent_A2.c_leak_data:
                            push = json.loads(most_recent_A2.p_leak_data)
                            coke = json.loads(most_recent_A2.c_leak_data)
                            try:
                                pLeaks = len(push['data'])
                            except:
                                pLeaks = 0
                            try:
                                cLeaks = len(coke['data'])
                            except:
                                cLeaks = 0
                        form_enteredA2 = True

                A3data = ""
                lids = ""
                offtakes = ""
                if formA3.exists():
                    most_recent_A3 = formA3[0]
                    if most_recent_A3.date == today:
                        A3data = most_recent_A3
                        if most_recent_A3.l_leak_json and most_recent_A3.om_leak_json:
                            lids = json.loads(most_recent_A3.l_leak_json)
                            offtakes = json.loads(most_recent_A3.om_leak_json)
                        form_enteredA3 = True

                A4data = ""
                if formA4.exists():
                    most_recent_A4 = formA4[0].date
                    if most_recent_A4 == today:
                        A4data = formA4[0]
                        form_enteredA4 = True

                A5data = ""
                if formA5.exists():
                    most_recent_A5 = formA5[0].form.date
                    if most_recent_A5 == today:
                        A5data = formA5[0]
                        form_enteredA5 = True
        else:
            formA4 = ""
            todays_log = ''

        if emypty_dp_today:
            if request.method == 'POST':
                answer = request.POST
                if answer['facilitySelect'] != '':
                    return redirect('sup_dashboard', answer['facilitySelect'])
            return render(request, "supervisor/sup_dashboard.html", {
                'notifs': notifs,
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
                'fsIDs': fsIDs,
                'quarterly_percent': quarterly_percent,
                'top7xValues': top7xValues,
                'top7yValues': top7yValues,
                'top7xValuesD': top7xValuesD,
                'top7yValuesD': top7yValuesD,
                'top7xValuesL': top7xValuesL,
                'top7yValuesL': top7yValuesL,
                'last7days': str(last7days),
                'today': str(now)
            })
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard', answer['facilitySelect'])
        
    return render(request, "supervisor/sup_dashboard.html", {
        'notifs': notifs,
        'facility': facility, 
        'form_enteredA5': form_enteredA5, 
        'form_enteredA4': form_enteredA4, 
        'form_enteredA3': form_enteredA3, 
        'form_enteredA2': form_enteredA2,
        'form_enteredA1': form_enteredA1, 
        'date': date, 
        "od_30": od_30, 
        "od_10": od_10, 
        "od_5": od_5, 
        'od_recent': od_recent, 
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
        'weekly_percent': weekly_percent, 
        'monthly_percent': monthly_percent, 
        'annually_percent': annually_percent, 
        'daily_percent': daily_percent,
        'quarterly_percent': quarterly_percent,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'sortedFacilityData': sortedFacilityData,
        'fsIDs': fsIDs,
        'top7xValues': top7xValues,
        'top7yValues': top7yValues,
        'top7xValuesD': top7xValuesD,
        'top7yValuesD': top7yValuesD,
        'top7xValuesL': top7xValuesL,
        'top7yValuesL': top7yValuesL,
        'last7days': str(last7days),
        'today': str(now),
        'pLeaks': pLeaks,
        'cLeaks': cLeaks
    })
