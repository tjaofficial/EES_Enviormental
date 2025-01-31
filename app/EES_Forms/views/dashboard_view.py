from django.shortcuts import render, redirect # type: ignore
from ..models import user_profile_model, Forms, daily_battery_profile_model, signature_model, bat_info_model, the_packets_model, form_settings_model
from ..utils import weatherDict, ninetyDayPushTravels, setUnlockClientSupervisor,userGroupRedirect, setUnlockClientSupervisor, get_facility_forms, updateAllFormSubmissions
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import re

lock = login_required(login_url='Login')

@lock
def IncompleteForms(request, facility):
    formName = "obs_dash"
    permissions = [OBSER_VAR]
    userGroupRedirect(request.user, permissions)
    if facility == OBSER_VAR:
        return redirect('facilitySelect', 'observer')
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = user_profile_model.objects.all()
    today = datetime.date.today()
    todays_num = today.weekday()
    today_str = str(today)
    now = datetime.datetime.now().date()
    signatures = signature_model.objects.all().order_by('-sign_date')
    sigExisting = False
    sigName = ''
    facilityData = bat_info_model.objects.filter(facility_name=facility)[0]
    facPackets = the_packets_model.objects.filter(facilityChoice__facility_name=facility)

    # ------- Signatures ---------------- 
    if signatures.exists():
        if signatures[0].sign_date == today:
            sigExisting = True
            sigName = signatures[0].supervisor
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
    def natural_sort_key(value):
        """Extracts numbers from alphanumeric keys for correct sorting."""
        return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', value)]

    packetQuery = the_packets_model.objects.filter(facilityChoice__facility_name=facility)

    for packet in packetQuery:
        # Ensure formList and formsList exist
        if hasattr(packet, "formList") and "formsList" in packet.formList:
            # Sort the dictionary keys naturally (A1, A2, ..., B, C, G1, G2, ...)
            packet.formList["sortedFormsList"] = sorted(
                packet.formList["formsList"].items(), key=lambda x: natural_sort_key(x[0])
            )







    facFormsIDList = get_facility_forms('facilityName', facility)
    facFormsSettingsModel = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    facFormList2 = []
    for facFormID in facFormsIDList:
        try:
            facFormList2.append(facFormsSettingsModel.get(id=int(facFormID)))
        except:
            continue

    facFormList1 = []
    for fsID in facFormList2:
        formInfo = fsID.formChoice
        if todays_num in [5,6] and formInfo.day_freq in ['5', '6', 'Weekends', 'Everyday']:
            if formInfo.weekend_only and not formInfo.weekdays_only or not formInfo.weekend_only and not formInfo.weekdays_only:
                facFormList1.append(fsID)
        elif todays_num in [0,1,2,3,4] and formInfo.day_freq in ['0','1','2','3','4','Weekdays','Everyday']:
            if formInfo.weekdays_only and not formInfo.weekend_only or not formInfo.weekdays_only and not formInfo.weekend_only:
                facFormList1.append(fsID)
    facFormList1.sort(key=lambda record: record.id)
    print(facFormList1)
    print("______________________")
    packetQuery2 = the_packets_model.objects.filter(facilityChoice__facility_name=facility)
    listOfAllPacketIDs = []
    for anID in packetQuery2:
        listOfAllPacketIDs.append(anID.id)

# ---------Update All Form Subs--------------------
    updateAllFormSubmissions(facility)

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
        #'sorting_array': sorting_array,
        "form_checkAll2": form_checkAll2,
        'sigExisting': sigExisting,
        'facility': facility,
        'sigName': sigName,
        'inopNumbsParse': inopNumbsParse,
        'facPackets': facPackets,
        'facFormList1': facFormList1,
        'packetQuery': packetQuery,
        'listOfAllPacketIDs': listOfAllPacketIDs,
        'formName': formName,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
    })

@lock
def default_dashboard(request, facility):
    permissions = [OBSER_VAR]
    userGroupRedirect(request.user, permissions)
    updateAllFormSubmissions(facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    packetsQuery = the_packets_model.objects.filter(facilityChoice__facility_name=facility)
    formData = Forms.objects.all()
    today = datetime.datetime.today().date()
    todaysName = today.strftime('%A')
    user = request.user
    userProfQuery = user_profile_model.objects.all()
    userCompany = userProfQuery.get(user=user).company
    facilityContacts = user_profile_model.objects.filter(facilityChoice__facility_name=facility)
    print(facilityContacts)

    return render(request, 'observer/dashboards/obs_default_dash.html', {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'packetsQuery': packetsQuery,
        'formData': formData,
        'todaysName': todaysName
    })