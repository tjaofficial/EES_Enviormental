from django.contrib.auth.decorators import login_required # type: ignore
from ..models import facility_model, issues_model, form1_model, form2_model, form3_model, Event, form4_model, form5_model, daily_battery_profile_model, user_profile_model
from ..utils.main_utils import weatherDict, calculateProgessBar, ninetyDayPushTravels
from django.template.loader import render_to_string  # type: ignore
from django.http import JsonResponse # type: ignore
import datetime
import calendar
import json

lock = login_required(login_url='Login')

@lock
def card_progress_bar(request, facility):
    options = facility_model.objects.filter(facility_name=facility)
    if options.exists():
        options = options.first()
    progress_data = request.user.user_profile.settings['facilities'][str(options.id)]['settings']['progressBar']
    daily_percent = calculateProgessBar(facility, 'Daily')
    weekly_percent = calculateProgessBar(facility, "Weekly")
    monthly_percent = calculateProgessBar(facility, 'Monthly')
    quarterly_percent = calculateProgessBar(facility, 'Quarterly')
    annually_percent = 0
    
    
    html = render_to_string(
        "shared/dashboard_cards/dashCard_progress.html", 
        {"progressBar": progress_data,
         'daily_percent': daily_percent,
         'weekly_percent': weekly_percent,
         'monthly_percent': monthly_percent,
         'quarterly_percent': quarterly_percent,
         'annually_percent': annually_percent}, 
        request=request
    )
    return JsonResponse({"html": html})

@lock
def card_daily_battery_forms(request, facility):
    now = datetime.datetime.now().date()
    formA1 = form1_model.objects.filter(formSettings__facilityChoice__facility_name=facility, date=now)
    formA2 = form2_model.objects.filter(formSettings__facilityChoice__facility_name=facility, date=now)
    formA3 = form3_model.objects.filter(formSettings__facilityChoice__facility_name=facility, date=now)
    formA4 = form4_model.objects.filter(formSettings__facilityChoice__facility_name=facility, date=now)
    formA5 = form5_model.objects.filter(formSettings__facilityChoice__facility_name=facility, date=now)
    A1data = formA1[0] if formA1.exists() else False
    A2data = formA2[0] if formA2.exists() else False
    A3data = formA3[0] if formA3.exists() else False
    A4data = formA4[0] if formA4.exists() else False
    A5data = formA5[0] if formA5.exists() else False
    
    html = render_to_string("shared/dashboard_cards/dashCard_batteryDailyForms.html", 
        {"A1data": A1data, 
         "A2data": A2data,
         "A3data": A3data, 
         "A4data": A4data, 
         "A5data": A5data,
         "now": str(now)}, 
        request=request
    )
    return JsonResponse({"html": html})

@lock
def card_graphs(request, facility):
    formA1 = form1_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    formA2 = form2_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    formA3 = form3_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    now = datetime.datetime.now().date()
    userProfile = request.user.user_profile
    options = facility_model.objects.filter(facility_name=facility)
    if options.exists():
        options = options.first()

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
                oneWeekAgo = now - datetime.timedelta(days=ranID)
                for x in range(0,ranID+1):
                    dateList.append(oneWeekAgo + datetime.timedelta(days=x))
            elif rangeID == 'monthly':
                ranID = calendar.monthrange(now.year,now.month)[1]
                for x in range(0,ranID):
                    dateList.append(datetime.datetime.strptime(str(now.year) + "-" + str(now.month) + "-01", "%Y-%m-%d").date() + datetime.timedelta(days=x))
            elif rangeID == 'annually':
                ranID = 365 + calendar.isleap(now.year)
                for x in range(0,ranID):
                    dateList.append(datetime.datetime.strptime(str(now.year) + "-" + "01-01", "%Y-%m-%d").date() + datetime.timedelta(days=x))
            else:
                ranID = abs((datetime.datetime.strptime(setGraphRange['dates']['graphStart'], "%Y-%m-%d").date() - datetime.datetime.strptime(setGraphRange['dates']['graphStop'], "%Y-%m-%d").date()).days)
                for x in range(0,ranID):
                    dateList.append(datetime.datetime.strptime(setGraphRange['dates']['graphStart'], "%Y-%m-%d").date() + datetime.timedelta(days=x))
            return dateList
        dateList = rangeNumber(setGraphRange['frequency'])
        print('hello')
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
                            xValues.append(float(useModel[0].ovens_data['total_seconds']))
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
            'today': str(now),
            'frequency': setGraphRange, 
        }
        graphDataDump = json.dumps(graphData)
        print(graphData)
    
    html = render_to_string(
        "shared/dashboard_cards/dashCard_graphs.html", 
        {'graphData': graphData, 'graphDataDump': graphDataDump, 'facility': facility}, 
        request=request
    )
    return JsonResponse({"html": html})

@lock
def card_corrective_actions(request, facility):
    ca_forms = issues_model.objects.filter(facilityChoice__facility_name=facility).order_by('-id')

    html = render_to_string(
        "shared/dashboard_cards/dashCard_correctiveActions.html", 
        {'ca_forms': ca_forms, 'facility': facility}, 
        request=request
    )
    return JsonResponse({"html": html})

@lock
def card_info(request, facility):
    now = datetime.datetime.now().date()
    options = facility_model.objects.filter(facility_name=facility)
    options = options.first() if options.exists() else False
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility, date_save=now)
    daily_prof = daily_prof.first() if daily_prof else False
    weather = weatherDict(False) if facility == 'supervisor' else weatherDict(options.city)
    
    todays_obser = 'Schedule Not Updated'
    event_cal = Event.objects.all()
    today = datetime.date.today()
    if event_cal.exists():
        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer

    html = render_to_string(
        "shared/dashboard_cards/dashCard_info.html", 
        {'weather': weather, "todays_log": daily_prof, 'facility': facility, 'todays_obser': todays_obser}, 
        request=request
    )
    return JsonResponse({"html": html})

@lock
def card_90DayPushTravels(request, facility):
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
    
    html = render_to_string(
        "shared/dashboard_cards/dashCard_90DayPushTravels.html", 
        {'od_5': od_5, 'od_10': od_10, 'od_30': od_30, 'facility': facility}, 
        request=request
    )
    return JsonResponse({"html": html})

@lock
def card_contacts(request, facility):
    allContacts = user_profile_model.objects.filter(company=request.user.user_profile.company)
    
    html = render_to_string(
        "shared/dashboard_cards/dashCard_contacts.html", 
        {'profile': allContacts}, 
        request=request
    )
    return JsonResponse({"html": html})
