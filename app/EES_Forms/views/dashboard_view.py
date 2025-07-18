from django.shortcuts import render, redirect # type: ignore
from ..models import user_profile_model, Forms, daily_battery_profile_model, signature_model, facility_model, the_packets_model, form_settings_model
from ..utils.main_utils import weatherDict, ninetyDayPushTravels, setUnlockClientSupervisor,userGroupRedirect, setUnlockClientSupervisor, updateAllFormSubmissions
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from EES_Enviormental.settings import OBSER_VAR
import re
from ..decor import group_required

lock = login_required(login_url='Login')

@lock
@group_required(OBSER_VAR)
def IncompleteForms(request):
    formName = "obs_dash"
    facility = getattr(request, 'facility', None)
    if not facility:
        return redirect('facilitySelect')
    today = datetime.date.today()
    todays_num = today.weekday()
    now = datetime.datetime.now().date()
    signatures = signature_model.objects.all().order_by('-sign_date')
    facPackets = the_packets_model.objects.filter(facilityChoice=facility)
    sigExisting = False
    sigName = ''

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
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice=facility, date_save=now).order_by('-date_save')
    profile_entered = False
    if daily_prof.exists():
        todays_log = daily_prof[0]
        profile_entered = True
    else:
        todays_log = ''
    inopNumbsParse = todays_log.inop_numbs.replace("'","").replace("[","").replace("]","") if todays_log else ''
    # --------Weather API Pull---------------
    weather = weatherDict(facility.city)
    # ---------Form Data--------------------
    def natural_sort_key(value):
        """Extracts numbers from alphanumeric keys for correct sorting."""
        return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', value)]


    #-----New Dashoard Filter-------
    packetList = []
    print(f"List of packets within {facility}: {facPackets}")
    for packet in facPackets:
        complete_forms = []
        incomplete_forms = []

        for key, fsID in packet.formList['formsList'].items():
            formSettings = form_settings_model.objects.get(id=fsID['settingsID'])
            formSubmitted = formSettings.subChoice.submitted
            formLabel = key
            formInfo = formSettings.formChoice

            if formSettings.settings['active']:
                if todays_num in [5,6] and formInfo.day_freq in ['5', '6', 'Weekends', 'Everyday']:
                    if formInfo.weekend_only and not formInfo.weekdays_only or not formInfo.weekend_only and not formInfo.weekdays_only:
                        if formSubmitted:
                            complete_forms.append((formSettings, formLabel))
                        else:
                            incomplete_forms.append((formSettings, formLabel))
                elif todays_num in [0,1,2,3,4] and formInfo.day_freq in ['0','1','2','3','4','Weekdays','Everyday']:
                    if formInfo.weekdays_only and not formInfo.weekend_only or not formInfo.weekdays_only and not formInfo.weekend_only:
                        if formSubmitted:
                            complete_forms.append((formSettings, formLabel))
                        else:
                            incomplete_forms.append((formSettings, formLabel))
        
        complete_forms.sort(key=lambda x: natural_sort_key(x[1] or ''))
        incomplete_forms.sort(key=lambda x: natural_sort_key(x[1] or ''))

        packetList.append({
            "packet": packet,
            "forms": {
                "complete": complete_forms,
                "incomplete": incomplete_forms
            }
        })


    allActiveFacFormsList = []
    allActiveFacForms = form_settings_model.objects.filter(settings__active=True, facilityChoice=facility)
    for items in allActiveFacForms:
        formInfo = items.formChoice
        if todays_num in [5,6] and formInfo.day_freq in ['5', '6', 'Weekends', 'Everyday']:
            if formInfo.weekend_only and not formInfo.weekdays_only or not formInfo.weekend_only and not formInfo.weekdays_only:
                allActiveFacFormsList.append(items)
        elif todays_num in [0,1,2,3,4] and formInfo.day_freq in ['0','1','2','3','4','Weekdays','Everyday']:
            if formInfo.weekdays_only and not formInfo.weekend_only or not formInfo.weekdays_only and not formInfo.weekend_only:
                allActiveFacFormsList.append(items)
    allActiveFacFormsList.sort(key=lambda x: natural_sort_key(str(x.id)))

    print(allActiveFacFormsList)
    listOfAllPacketIDs = []
    for anID in facPackets:
        listOfAllPacketIDs.append(anID.id)

# ---------Update All Form Subs--------------------
    updateAllFormSubmissions(facility)

    return render(request, "observer/obs_dashboard.html", {
        'od_recent': od_recent, 
        "todays_log": todays_log, 
        'now': now, 
        'profile_entered': profile_entered, 
        'todays_num': todays_num, 
        'weather': weather, 
        'sigExisting': sigExisting,
        'facility': facility,
        'sigName': sigName,
        'inopNumbsParse': inopNumbsParse,
        'facPackets': facPackets,
        'listOfAllPacketIDs': listOfAllPacketIDs,
        'formName': formName,
        'packetList': packetList,
        'allActiveFacFormsList': allActiveFacFormsList
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