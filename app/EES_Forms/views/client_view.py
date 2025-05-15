from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..models import issues_model, form1_model, form2_model, form3_model, Event, form4_model, form5_model, daily_battery_profile_model, User, user_profile_model, facility_model
from ..decor import group_required
import datetime
import json
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils.main_utils import userColorMode, colorModeSwitch, setUnlockClientSupervisor, weatherDict, calculateProgessBar, getCompanyFacilities,checkIfFacilitySelected, userGroupRedirect, tryExceptFormDatabases,updateAllFormSubmissions, ninetyDayPushTravels

lock = login_required(login_url='Login')

@lock
@group_required(CLIENT_VAR)
def client_dashboard_view(request):
    facility = getattr(request, 'facility', None)
    updateAllFormSubmissions(facility)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    formA1 = form1_model.objects.filter(formSettings__facilityChoice=facility).order_by('-date')
    formA2 = form2_model.objects.filter(formSettings__facilityChoice=facility).order_by('-date')
    formA3 = form3_model.objects.filter(formSettings__facilityChoice=facility).order_by('-date')
    formA4 = form4_model.objects.filter(formSettings__facilityChoice=facility).order_by('-date')
    formA5 = form5_model.objects.filter(formSettings__facilityChoice=facility).order_by('-date')
    fsID1 = tryExceptFormDatabases(1,formA1, facility)
    fsID2 = tryExceptFormDatabases(2,formA2, facility) 
    fsID3 = tryExceptFormDatabases(3,formA3, facility)
    fsID4 = tryExceptFormDatabases(4,formA4, facility)
    fsID5 = tryExceptFormDatabases(5,formA5, facility)
    fsIDs = [fsID1,fsID2,fsID3,fsID4,fsID5]
    
    now = datetime.datetime.now().date()

    last7days = now - datetime.timedelta(days=6)
    options = facility
    emypty_dp_today = True
    colorMode = userColorMode(request.user)[0]  
    userMode = userColorMode(request.user)[1]
    userProfile = request.user.user_profile
    userCompany = userProfile.company

    today = datetime.date.today()
    #---------- Graph Data ---------------------
    graphData = ''
    graphDataDump = ''
    if facility:
        if userProfile.settings['facilities'][str(options.id)]['dashboard'] == "Battery":
            baseIterations = userProfile.settings['facilities'][str(options.id)]['settings']
            graphSettings = baseIterations['graphs']
            setGraphRange = graphSettings['graphFrequencyData']
        
            canvasData = {}
            dateList = []
            def rangeNumber(rangeID):
                dateList = []
                if rangeID == 'weekly':
                    ranID = 6
                    oneWeekAgo = today - datetime.timedelta(days=ranID)
                    for x in range(0,ranID+1):
                        dateList.append(oneWeekAgo + datetime.timedelta(days=x))
                elif rangeID == 'monthly':
                    ranID = calendar.monthrange(today.year,today.month)[1]
                    for x in range(0,ranID):
                        dateList.append(datetime.datetime.strptime(str(today.year) + "-" + str(today.month) + "-01", "%Y-%m-%d").date() + datetime.timedelta(days=x))
                elif rangeID == 'annually':
                    ranID = 365 + calendar.isleap(today.year)
                    for x in range(0,ranID):
                        dateList.append(datetime.datetime.strptime(str(today.year) + "-" + "01-01", "%Y-%m-%d").date() + datetime.timedelta(days=x))
                else:
                    ranID = abs((datetime.datetime.strptime(setGraphRange['dates']['graphStart'], "%Y-%m-%d").date() - datetime.datetime.strptime(setGraphRange['dates']['graphStop'], "%Y-%m-%d").date()).days)
                    for x in range(0,ranID):
                        dateList.append(datetime.datetime.strptime(setGraphRange['dates']['graphStart'], "%Y-%m-%d").date() + datetime.timedelta(days=x))
                return dateList
            dateList = rangeNumber(setGraphRange['frequency'])
            print(dateList)
            for gStuff in graphSettings['dataChoice']:
                if gStuff == 'graph90dayPT':
                    continue
                if graphSettings['dataChoice'][gStuff]['show']:
                    canvasData[gStuff] = {
                        'graphID': gStuff,
                        'xValues': [],
                        'yValues': [],
                        'type': graphSettings['dataChoice'][gStuff]['type'],
                    }
                    xValues = []
                    yValues = []
                    for dates in dateList:
                        if gStuff == 'charges':
                            useModel = formA1.filter(date=dates)
                            if useModel.exists():
                                xValues.append(int(useModel[0].ovens_data['total_seconds']))
                                yValues.append(str(useModel[0].date))
                        elif gStuff == 'doors':
                            useModel = formA2.filter(date=dates)
                            if useModel.exists():
                                xValues.append(int(useModel[0].leaking_doors))
                                yValues.append(str(useModel[0].date))
                        elif gStuff == 'lids':
                            useModel = formA3.filter(date=dates)
                            if useModel.exists():
                                xValues.append(int(useModel[0].l_leaks))
                                yValues.append(str(useModel[0].date))
                        if str(dates) not in yValues:
                            xValues.append(int(0))
                            yValues.append(str(dates))
                    canvasData[gStuff]['xValues'] = xValues
                    canvasData[gStuff]['yValues'] = yValues
            graphData = {
                'canvasData': canvasData,
                'today': str(today),
                'frequency': setGraphRange, 
            }
            graphDataDump = json.dumps(graphData)
    # -------PROGRESS PERCENTAGES -----------------
    if facility:
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
    if facility:
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
    else:
        od_recent = ''
        od_30 = ''
        od_10 = ''
        od_5 = ''
    # ----CONTACTS-----------------
    allContacts = user_profile_model.objects.filter(company=userCompany)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    # ----USER ON SCHEDULE----------
    todays_obser = 'Schedule Not Updated'
    event_cal = Event.objects.all()
    today = datetime.date.today()
    if event_cal.exists():
        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer
    # ----ISSUES/CORRECTIVE ACTIONS----------
    ca_forms = issues_model.objects.filter(formChoice=facility).order_by('-id')
    # ----Weather API Pull-----------
    if not facility:
        weather = weatherDict(False)
    else:
        weather = weatherDict(options.city)
    # ----OTHER-----------    
    if request.user.groups.filter(name=CLIENT_VAR) or request.user.is_superuser:
        if emypty_dp_today:
            if request.method == 'POST':
                answer = request.POST
                if 'colorMode' in answer.keys():
                    print("CHECK 1")
                    colorModeSwitch(request)
                    return redirect(request.META['HTTP_REFERER'])
            return render(request, "supervisor/sup_dashboard.html", {
                'notifs': notifs,
                'facility': facility, 
                'ca_forms': ca_forms, 
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
                'graphData': graphData,
                'last7days': str(last7days),
                'today': str(now),
                'colorMode': colorMode,
                'userMode': userMode,
                'options': options,
                'graphDataDump': graphDataDump,
                "od_30": od_30, 
                "od_10": od_10, 
                "od_5": od_5, 
                'userProfile': userProfile
            })
    if request.method == 'POST':
        answer = request.POST
        if 'colorMode' in answer.keys():
            print(answer['colorMode'])
            colorModeSwitch(request)
        
    return render(request, "supervisor/sup_dashboard.html", {
        'notifs': notifs,
        'facility': facility, 
        'options': options,
        'userProfile': userProfile
    })
