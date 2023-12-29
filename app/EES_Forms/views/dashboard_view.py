from django.shortcuts import render, redirect
from ..models import user_profile_model, formA5_readings_model, Forms, daily_battery_profile_model, signature_model, formG2_model, bat_info_model, facility_forms_model, formSubmissionRecords_model
from ..utils import weatherDict, ninetyDayPushTravels, setUnlockClientSupervisor
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime
import requests
import calendar
import ast
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

lock = login_required(login_url='Login')


@lock
def IncompleteForms(request, facility):
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if supervisor:
        return redirect('sup_dashboard', facility)
    elif client:
        return redirect('c_dashboard')
    
    profile = user_profile_model.objects.all()
    today = datetime.date.today()
    todays_num = today.weekday()
    sub_forms = Forms.objects.all()
    reads = formA5_readings_model.objects.all()
    today_str = str(today)
    now = datetime.datetime.now().date()
    weekday_fri = today + datetime.timedelta(days=4 - todays_num)
    weekend_fri = weekday_fri + datetime.timedelta(days=7)
    signatures = signature_model.objects.all().order_by('-sign_date')
    sigExisting = False
    sigName = ''
    facilityData = bat_info_model.objects.filter(facility_name=facility)[0]

    if signatures.exists():
        if signatures[0].sign_date == today:
            sigExisting = True
            sigName = signatures[0].supervisor
    def what_quarter(input):
        if input.month in {1,2,3}:
            return 1
        if input.month in {4,5,6}:
            return 2
        if input.month in {7,8,9}:
            return 3
        if input.month in {10,11,12}:
            return 4
        

    def monthDayAdjust(input):
        if len(str(input)) == 1:
            return '0'+str(input)
        else:
            return str(input)
# ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
# ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
    if Forms.objects.count() <= 5:
        A1 = Forms(
            form=1,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA1",
            header="Method 303",
            title="Charging",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A2 = Forms(
            form=2,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA2",
            header="Method 303",
            title="Doors",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A3 = Forms(
            form=3,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA3",
            header="Method 303",
            title="Lids and Offtakes",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A4 = Forms(
            form=4,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA4",
            header="Method 303",
            title="Collection Main",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        A5 = Forms(
            form=5,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formA5",
            header="Method 9B",
            title="Push Travels",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        B = Forms(
            form=6,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="formB",
            header="Method 9",
            title="Fugitive Dust Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        C = Forms(
            form=7,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formC",
            header="Method 9",
            title="Method 9D - Coal Field",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        D = Forms(
            form=8,
            frequency="Weekly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formD",
            header="Method 9",
            title="Random Truck Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        E = Forms(
            form=9,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formE",
            header="Method 9",
            title="Gooseneck Inspection",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F1 = Forms(
            form=10,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF1",
            header="Waste Weekly Inspections",
            title="SIF / K087 Process Area (Satellite)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F2 = Forms(
            form=11,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF2",
            header="Waste Weekly Inspections",
            title="#1 Shop (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F3 = Forms(
            form=12,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF3",
            header="Waste Weekly Inspections",
            title="#2 Shop (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F4 = Forms(
            form=13,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF4",
            header="Waste Weekly Inspections",
            title="Battery (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F5 = Forms(
            form=14,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF5",
            header="Waste Weekly Inspections",
            title="Bio Plant (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F6 = Forms(
            form=15,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF6",
            header="Waste Weekly Inspections",
            title="No. 8 Tank Area (Satellite Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        F7 = Forms(
            form=16,
            frequency="Weekly",
            day_freq='Wednesdays',
            weekdays_only=False,
            weekend_only=False,
            link="formF7",
            header="Waste Weekly Inspections",
            title="Booster Pad (90-Day Accumulation)",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        G1 = Forms(
            form=17,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formG1",
            header="PECS Baghouse Stack",
            title="Method 9/Non-Certified Observations",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        G2 = Forms(
            form=18,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formG2",
            header="PECS Baghouse Stack",
            title="Method 9B",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        H = Forms(
            form=19,
            frequency="Weekly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formH",
            header="Method 9",
            title="Method 9 - Combustion Stack",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        I = Forms(
            form=20,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="formI",
            header="Sampling",
            title="Quench Water Sampling Form",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        L = Forms(
            form=21,
            frequency="Daily",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="formL",
            header="Method 9",
            title="Visual Emissions Observations",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        M = Forms(
            form=22,
            frequency="Daily",
            day_freq='Weekdays',
            weekdays_only=True,
            weekend_only=False,
            link="formM",
            header="Method 9D",
            title="Method 9D Observation",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        N = Forms(
            form=23,
            frequency="Monthly",
            day_freq='Weekdays',
            weekdays_only=False,
            weekend_only=False,
            link="formN",
            header="Fugitive Dust Inspection",
            title="Method 9D Monthly Checklist",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        O = Forms(
            form=24,
            frequency="Weekly",
            day_freq='Weekends',
            weekdays_only=False,
            weekend_only=True,
            link="formO",
            header="Stormwater Observation Form",
            title="MP 108A",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        P = Forms(
            form=25,
            frequency="Weekly",
            day_freq='Weekends',
            weekdays_only=False,
            weekend_only=True,
            link="formP",
            header="Outfall Observation Form",
            title="Outfall 008",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        spill_kits = Forms(
            form=26,
            frequency="Monthly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="spill_kits",
            header="Spill Kits Form",
            title="Inspection Check List",
            due_date=today,
            date_submitted=today - datetime.timedelta(days=1),
            submitted=False,)
        quarterly_trucks = Forms(
            form=27,
            frequency="Quarterly",
            day_freq='Everyday',
            weekdays_only=False,
            weekend_only=False,
            link="quarterly_trucks",
            header="Quarterly Trucks Form",
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
        quarterly_trucks.save()

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
# -------Battery Profile Data------------
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    profile_entered = False
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if now == todays_log.date_save:
            profile_entered = True
    else:
        todays_log = ''
# --------Weather API Pull---------------
    weather = weatherDict(facilityData.city)
# ---------Form Data--------------------
    if facility_forms_model.objects.filter(facilityChoice__facility_name=facility).exists():
        facilityFroms = ast.literal_eval(facility_forms_model.objects.filter(facilityChoice__facility_name=facility)[0].formData)
    if formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility).exists():
        facilitySubs = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    
    all_incomplete_forms = []
    all_complete_forms = []
    daily_incomplete_forms = []
    daily_complete_forms = []
    weekly_incomplete_forms = []
    weekly_complete_forms = []
    monthly_incomplete_forms = []
    monthly_complete_forms = []
    quarterly_incomplete_forms = []
    quarterly_complete_forms = []
    annual_incomplete_forms = []
    annual_complete_forms = []
    sannual_incomplete_forms = []
    sannual_complete_forms = []
        
    for forms in facilityFroms:
        for sub in facilitySubs:
            if forms[0] == sub.formID.id:
                sub.submitted = True
                if sub.formID.frequency == 'Monthly':
                    numbOfDaysInMonth = calendar.monthrange(today.year, today.month)[1]
                    lastDayOfMonth = str(today.year) + '-' + str(today.month) + '-' + str(numbOfDaysInMonth)
                    sub.dueDate = datetime.datetime.strptime(lastDayOfMonth, "%Y-%m-%d").date()
                    dueDate = sub.dueDate
                    if sub.dateSubmitted.year != dueDate.year or sub.dateSubmitted.month != dueDate.month:
                        sub.submitted = False
                    elif sub.dateSubmitted.day > numbOfDaysInMonth:
                        sub.submitted = False
                    sub.save()
                elif sub.formID.frequency == 'Quarterly':
                    if what_quarter(today) == 1:
                        monthDue = 3
                        yearDue = today.year
                        dayDue =  calendar.monthrange(yearDue, monthDue)[1]
                    elif what_quarter(today) == 2:
                        monthDue = 6
                        yearDue = today.year
                        dayDue =  calendar.monthrange(yearDue, monthDue)[1]
                    elif what_quarter(today) == 3:
                        monthDue = 9
                        yearDue = today.year
                        dayDue =  calendar.monthrange(yearDue, monthDue)[1]
                    elif what_quarter(today) == 4:
                        monthDue = 12
                        yearDue = today.year
                        dayDue =  calendar.monthrange(yearDue, monthDue)[1]
                    dateBuild = str(yearDue) + '-' + monthDayAdjust(monthDue) + '-' + monthDayAdjust(dayDue)
                    sub.dueDate = datetime.datetime.strptime(dateBuild, "%Y-%m-%d").date()
                    A = sub.dateSubmitted
                    B = sub.dueDate
                    if what_quarter(A) != what_quarter(B):
                        sub.submitted = False
                    sub.save()
                elif sub.formID.frequency == 'Weekly':
                    if todays_num in {0, 1, 2, 3, 4}:
                        print('CHECK 1')
                        sub.dueDate = weekday_fri
                        start_sat = weekday_fri - datetime.timedelta(days=6)
                    else:
                        sub.dueDate = weekend_fri
                        start_sat = today - datetime.timedelta(days= todays_num - 5)
                    A = sub.dateSubmitted
                    B = sub.dueDate
                    if sub.formID.day_freq == 'Weekends' and A != today:
                        sub.submitted = False   
                    elif A < start_sat or A > sub.dueDate:
                        sub.submitted = False
                    sub.save()
                elif sub.formID.frequency == 'Daily':
                    print(sub.formID)
                    if sub.formID.weekend_only and todays_num not in {5,6}:
                        print("CHECK 1")
                        print(sub.submitted)
                        sub.save()
                        continue
                    else:    
                        print("CHECK 2")
                        sub.dueDate = today
                        A = sub.dateSubmitted
                        B = sub.dueDate
                        if today != A:
                            print("CHECK 3")
                            sub.submitted = False
                        sub.save()
                        print(sub.submitted)
                    
                if sub.formID.day_freq in {'Everyday', todays_num} or (todays_num in {5, 6} and sub.formID.day_freq == 'Weekends') or (todays_num in {0, 1, 2, 3, 4} and sub.formID.day_freq == 'Weekdays'):
                    if sub.submitted == False:
                        if sub.formID.id in {17,18}:
                            if len(facilitySubs.filter(formID__id=18)) > 0:
                                g2_form = facilitySubs.filter(formID__id=18)[0]
                                startOfWeek = weekday_fri - datetime.timedelta(days=6)
                                if g2_form.submitted == True and startOfWeek <= g2_form.dateSubmitted <= weekday_fri:
                                    continue
                                else:
                                    all_incomplete_forms.append((sub, forms[1]))
                            else:
                                all_incomplete_forms.append((sub, forms[1]))
                        else:
                            all_incomplete_forms.append((sub, forms[1]))
                        if sub.formID.frequency == 'Daily':
                            daily_incomplete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Weekly':
                            weekly_incomplete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Monthly':
                            monthly_incomplete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Quarterly':
                            quarterly_incomplete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Annual':
                            annual_incomplete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Semi-Annual':
                            sannual_incomplete_forms.append((sub, forms[1]))
                    elif sub.submitted == True: 
                        all_complete_forms.append((sub, forms[1]))
                        if sub.formID.frequency == 'Daily':
                            daily_complete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Weekly':
                            weekly_complete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Monthly':
                            monthly_complete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Quarterly':
                            quarterly_complete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Annual':
                            annual_complete_forms.append((sub, forms[1]))
                        elif sub.formID.frequency == 'Semi-Annual':
                            sannual_complete_forms.append((sub, forms[1]))
                
    sorting_array = [
        all_incomplete_forms,
        all_complete_forms,
        daily_incomplete_forms,
        daily_complete_forms,
        weekly_incomplete_forms,
        weekly_complete_forms,
        monthly_incomplete_forms,
        monthly_complete_forms,
        quarterly_incomplete_forms,
        quarterly_complete_forms,
        annual_incomplete_forms,
        annual_complete_forms,
        sannual_incomplete_forms,
        sannual_complete_forms,
    ]

    if todays_num == 6:
        saturday = False
    else:
        saturday = True

    weekend_list = [5, 6]
    form_check1 = ["", ]
    form_check2 = ["", ]
    form_checkAll = ["", ]
    form_checkAll2 = ["", ]
    form_checkDaily2 = ["", ]
    
    inopNumbsParse = todays_log.inop_numbs.replace("'","").replace("[","").replace("]","")

    return render(request, "observer/obs_dashboard.html", {
        'form_checkDaily2': form_checkDaily2, 
        'form_checkAll': form_checkAll, 
        "today": today, 
        'od_recent': od_recent, 
        "todays_log": todays_log, 
        'now': now, 
        'profile_entered': profile_entered, 
        'form_check1': form_check1, 
        'form_check2': form_check2, 
        'profile': profile, 
        'today_str': today_str, 
        'todays_num': todays_num, 
        'weekend_list': weekend_list, 
        'weather': weather, 
        'saturday': saturday, 
        'sorting_array': sorting_array,
        "form_checkAll2": form_checkAll2,
        'sigExisting': sigExisting,
        'facility': facility,
        'sigName': sigName,
        'inopNumbsParse': inopNumbsParse
    })
