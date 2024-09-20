from django.shortcuts import render, redirect
from ..models import user_profile_model, form5_readings_model, Forms, daily_battery_profile_model, signature_model, form18_model, bat_info_model, facility_forms_model, formSubmissionRecords_model, the_packets_model, form_settings_model
from ..utils import weatherDict, ninetyDayPushTravels, setUnlockClientSupervisor,userGroupRedirect, setUnlockClientSupervisor2, create_starting_forms,get_facility_forms, updateAllFormSubmissions, checkIfFacilitySelected
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
    permissions = [OBSER_VAR]
    userGroupRedirect(request.user, permissions)
    unlock, client, supervisor = setUnlockClientSupervisor2(request.user)
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

    if signatures.exists():
        if signatures[0].sign_date == today:
            sigExisting = True
            sigName = signatures[0].supervisor
    # If there are less than 5 forms when first starting this program
    # this will create the base forms for EES Coke.
    create_starting_forms()
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
    facFormsIDList = get_facility_forms('facilityName', facility)
    facFormsSettingsModel = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    facFormList1 = []
    for facFormID in facFormsIDList:
        for formSetting in facFormsSettingsModel:
            if int(facFormID) == formSetting.id:
                facFormList1.append(formSetting)

    packetQuery = the_packets_model.objects.filter(facilityChoice__facility_name=facility)
    listOfAllPacketIDs = []
    for anID in packetQuery:
        listOfAllPacketIDs.append(anID.id)

# ---------Update All Form Subs--------------------
    updateAllFormSubmissions(facility)      
#---------------Old sorting stuff-----------------------
    # if facility_forms_model.objects.filter(facilityChoice__facility_name=facility).exists():
    #     facilityFroms = ast.literal_eval(facility_forms_model.objects.filter(facilityChoice__facility_name=facility)[0].formData)
    # # if formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility).exists():
    # #     facilitySubs = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    # print(facilityFroms)
    # all_incomplete_forms = []
    # all_complete_forms = []
    # daily_incomplete_forms = []
    # daily_complete_forms = []
    # weekly_incomplete_forms = []
    # weekly_complete_forms = []
    # monthly_incomplete_forms = []
    # monthly_complete_forms = []
    # quarterly_incomplete_forms = []
    # quarterly_complete_forms = []
    # annual_incomplete_forms = []
    # annual_complete_forms = []
    # sannual_incomplete_forms = []
    # sannual_complete_forms = []
        
    # for forms in facilityFroms:
    #     print(forms)
    #     for sub in facilitySubs:
    #         if forms == sub.formID.id:
    #             sub.submitted = True
    #             if sub.formID.day_freq in {'Everyday', todays_num} or (todays_num in {5, 6} and sub.formID.day_freq == 'Weekends') or (todays_num in {0, 1, 2, 3, 4} and sub.formID.day_freq == 'Weekdays'):
    #                 if sub.submitted == False:
    #                     if sub.formID.id in {17,18}:
    #                         if len(facilitySubs.filter(formID__id=18)) > 0:
    #                             g2_form = facilitySubs.filter(formID__id=18)[0]
    #                             startOfWeek = weekday_fri - datetime.timedelta(days=6)
    #                             if g2_form.submitted == True and startOfWeek <= g2_form.dateSubmitted <= weekday_fri:
    #                                 continue
    #                             else:
    #                                 all_incomplete_forms.append((sub, forms[1]))
    #                         else:
    #                             all_incomplete_forms.append((sub, forms[1]))
    #                     else:
    #                         all_incomplete_forms.append((sub, forms[1]))
    #                     if sub.formID.frequency == 'Daily':
    #                         daily_incomplete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Weekly':
    #                         weekly_incomplete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Monthly':
    #                         monthly_incomplete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Quarterly':
    #                         quarterly_incomplete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Annual':
    #                         annual_incomplete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Semi-Annual':
    #                         sannual_incomplete_forms.append((sub, forms[1]))
    #                 elif sub.submitted == True: 
    #                     all_complete_forms.append((sub, forms[1]))
    #                     if sub.formID.frequency == 'Daily':
    #                         daily_complete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Weekly':
    #                         weekly_complete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Monthly':
    #                         monthly_complete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Quarterly':
    #                         quarterly_complete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Annual':
    #                         annual_complete_forms.append((sub, forms[1]))
    #                     elif sub.formID.frequency == 'Semi-Annual':
    #                         sannual_complete_forms.append((sub, forms[1]))
                
    # sorting_array = [
    #     all_incomplete_forms,
    #     all_complete_forms,
    #     daily_incomplete_forms,
    #     daily_complete_forms,
    #     weekly_incomplete_forms,
    #     weekly_complete_forms,
    #     monthly_incomplete_forms,
    #     monthly_complete_forms,
    #     quarterly_incomplete_forms,
    #     quarterly_complete_forms,
    #     annual_incomplete_forms,
    #     annual_complete_forms,
    #     sannual_incomplete_forms,
    #     sannual_complete_forms,
    # ]

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
        'listOfAllPacketIDs': listOfAllPacketIDs
    })

@lock
def default_dashboard(request, facility):
    permissions = [OBSER_VAR]
    userGroupRedirect(request.user, permissions)
    updateAllFormSubmissions(facility)
    unlock, client, supervisor = setUnlockClientSupervisor2(request.user)
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