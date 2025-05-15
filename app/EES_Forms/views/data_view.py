from django.shortcuts import render, redirect # type: ignore
import datetime
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..models import form3_model, form1_model, form2_model, user_profile_model, daily_battery_profile_model, form5_model, Forms
from django.apps import apps # type: ignore
from ..utils.main_utils import ninetyDayPushTravels, setUnlockClientSupervisor, getCompanyFacilities
from django.contrib.auth.decorators import login_required # type: ignore


profile = user_profile_model.objects.all()
lock = login_required(login_url='Login')

@lock
def pt_admin1_view(request, facility):
    facility = getattr(request, 'facility', None)
    print(facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    allForms = Forms.objects.all()
    today = datetime.date.today()
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    data = form5_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    def checkIfAllNone(theGroup):
        dayCount = 0
        for ovenData in theGroup:
            if ovenData[1] == 'N/A':
                dayCount += 1
        if dayCount > 0:
            newList = []
        return newList
    # -------90 DAY PUSH ----------------
    all_db_reads = form5_model.objects.all()
    pushTravelsData = ninetyDayPushTravels(facility)
    print(pushTravelsData['all'])
    od_30 = pushTravelsData['30days']
    od_10 = pushTravelsData['10days']
    od_5 = pushTravelsData['5days']
    od_recent = pushTravelsData['closest']
    all_ovens = pushTravelsData['all']
    
    if request.method == 'POST':
        answer = request.POST
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard', answer['facilitySelect'])

    return render(request, "shared/PushTravels.html", {
        'facility': facility, 
        "now": now, 
        'todays_log': todays_log, 
         
        'reads': all_db_reads, 
        'data': data, 
        'cool': all_ovens, 
        'od_30': od_30, 
        'od_10': od_10, 
        'od_5': od_5, 
        'od_recent': od_recent, 
        "today": today, 
        'profile': profile, 
        'client': client, 
        "supervisor": supervisor, 
        "unlock": unlock, 
        'allForms': allForms,
        'sortedFacilityData': sortedFacilityData, 
    })

@lock
def pt_mth_input(request, facility):
    submitted_ordered = form5_model.objects.all()
    now = datetime.datetime.now()
    today = datetime.date.today()

    def pt_sort(submitted_ordered):
        A = []
        for x in submitted_ordered:
            date = x.date
            i = 1
            h = i+1
            j = i+2
            k = i+4
            A.append((
                date,
                x.o1,
                x.o1_start,
                x.o1_1_reads,
                x.o1_2_reads,
                x.o1_3_reads,
                x.o1_4_reads,
                x.o1_5_reads,
                x.o1_6_reads,
                x.o1_7_reads,
                x.o1_8_reads,
                x.o1_9_reads,
                x.o1_10_reads,
                x.o1_11_reads,
                x.o1_12_reads,
                x.o1_13_reads,
                x.o1_14_reads,
                x.o1_15_reads,
                x.o1_16_reads,
                'lightblue',
                i
            ))
            A.append((
                date,
                x.o2,
                x.o2_start,
                x.o2_1_reads,
                x.o2_2_reads,
                x.o2_3_reads,
                x.o2_4_reads,
                x.o2_5_reads,
                x.o2_6_reads,
                x.o2_7_reads,
                x.o2_8_reads,
                x.o2_9_reads,
                x.o2_10_reads,
                x.o2_11_reads,
                x.o2_12_reads,
                x.o2_13_reads,
                x.o2_14_reads,
                x.o2_15_reads,
                x.o2_16_reads,
                'skyblue',
                h
            ))
            A.append((
                date,
                x.o3,
                x.o3_start,
                x.o3_1_reads,
                x.o3_2_reads,
                x.o3_3_reads,
                x.o3_4_reads,
                x.o3_5_reads,
                x.o3_6_reads,
                x.o3_7_reads,
                x.o3_8_reads,
                x.o3_9_reads,
                x.o3_10_reads,
                x.o3_11_reads,
                x.o3_12_reads,
                x.o3_13_reads,
                x.o3_14_reads,
                x.o3_15_reads,
                x.o3_16_reads,
                'lightblue',
                j
            ))
            A.append((
                date,
                x.o4,
                x.o4_start,
                x.o4_1_reads,
                x.o4_2_reads,
                x.o4_3_reads,
                x.o4_4_reads,
                x.o4_5_reads,
                x.o4_6_reads,
                x.o4_7_reads,
                x.o4_8_reads,
                x.o4_9_reads,
                x.o4_10_reads,
                x.o4_11_reads,
                x.o4_12_reads,
                x.o4_13_reads,
                x.o4_14_reads,
                x.o4_15_reads,
                x.o4_16_reads,
                'skyblue',
                k
            ))
            i += 4
        return A

    new_A5_list = pt_sort(submitted_ordered)

    func = lambda x: (x[0])
    sort = sorted(new_A5_list, key=func, reverse=True)

    return render(request, "ees_forms/pt_mth_input.html", {
        'facility': facility, "now": now,  "today": today, 'submitted_ordered': submitted_ordered, 'sort': sort, 'profile': profile,
    })

@lock
def method303_rolling_avg(request, facility):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    daily_prof = daily_battery_profile_model.objects.all().order_by('date_save')
    todays_log = daily_prof[0]
    now = datetime.datetime.now()
    today = datetime.date.today()
    A = []
    print("hello")
    def form_compile(daily_prof):
        formA1 = form1_model.objects.all()
        formA2 = form2_model.objects.all()
        formA3 = form3_model.objects.all()
        i = 1
        print("CHECK 1")
        for date_select in daily_prof:
            for logA1 in formA1:
                if str(date_select.date_save) == str(logA1.date):
                    A1 = logA1

                    for logA2 in formA2:
                        if date_select.date_save == logA2.date:
                            A2 = logA2

                            for logA3 in formA3:
                                if date_select.date_save == logA3.date:
                                    A3 = logA3

                                    A.append((i, date_select.date_save, A1.c1_sec, A1.c2_sec, A1.c3_sec, A1.c4_sec, A1.c5_sec, A2.inop_ovens, A2.doors_not_observed, A2.leaking_doors, A3.inop_ovens, A3.l_not_observed, A3.l_leaks, A3.om_not_observed, A3.om_leaks))
                                    print(i)
                                    i += 1
        return A

    list_of_records = form_compile(daily_prof)
    
    # if request.method == "POST":
    parseFromList = [
        (1, "A1"),
        (2, "A2"),
        (3, "A3"),
        (4, "A4"),
        (5, "A5"),
        (6, "B"),
        (7, "C"),
        (8, "D"),
        (9, "E"),
        (10, "F1"),
        (11, "F2"),
        (12, "F3"),
        (13, "F4"),
        (14, "F5"),
        (15, "F6"),
        (16, "F7"),
        (17, "G1"),
        (18, "G1"),
        (19, "H"),
        (20, "I"),
        (21, "L"),
        (22, "M"),
        (23, "N"),
        (24, "O"),
        (25, "P"),
        (26, "R"),
        (27, "Q"),  
    ]
    for x in parseFromList:
        modelName = "form"+x[1]+"_model"
        formID = int(x[0])
        print(modelName)
        print("___________________________")
        existingModelData = apps.get_model('EES_Forms', modelName).objects.all()
        for y in existingModelData:
            print(y)
            break
                
            
        

    return render(request, "ees_forms/method303_rolling_avg.html", {
        'facility': facility, "now": now, 'todays_log': todays_log,  "today": today, 'list_of_records': list_of_records, 'profile': profile,
    })
