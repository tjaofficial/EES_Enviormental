from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ..forms import CreateUserForm, user_profile_form, bat_info_form
from ..models import bat_info_model, issues_model, formA1_readings_model, formA2_model, formA3_model, Event, formA4_model, formA5_readings_model, daily_battery_profile_model, User, user_profile_model, company_model
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
import json
from ..utils import setUnlockClientSupervisor, weatherDict, calculateProgessBar, ninetyDayPushTravels, colorModeSwitch, userColorMode, checkIfFacilitySelected, getCompanyFacilities, checkIfMoreRegistrations
from ..decor import isSubActive

lock = login_required(login_url='Login')

@lock
@isSubActive
def sup_dashboard_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    formA1 = formA1_readings_model.objects.filter(form__facilityChoice__facility_name=facility).order_by('-form')
    formA2 = formA2_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    formA3 = formA3_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    formA4 = formA4_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    formA5 = formA5_readings_model.objects.filter(form__facilityChoice__facility_name=facility).order_by('-form')
    reads = formA5_readings_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    now = datetime.datetime.now().date()
    options = bat_info_model.objects.filter(facility_name=facility)
    emypty_dp_today = True
    colorMode = userColorMode(request.user)[0]  
    userMode = userColorMode(request.user)[1]
    userProfile = user_profile_model.objects.get(user__id=request.user.id)
    userCompany = userProfile.company
    print(colorMode)
    
    if options.exists():
        options = options[0]
    
    if facility != 'supervisor':
        recent_logs = formA1_readings_model.objects.filter(form__facilityChoice__facility_name=facility).order_by('-form')[:7]
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
    if event_cal.exists():
        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer
    # ----ISSUES/CORRECTIVE ACTIONS----------
    ca_forms = issues_model.objects.filter(facilityChoice__facility_name=facility).order_by('-id')
    # ----Weather API Pull-----------
    if facility == 'supervisor':
        weather = weatherDict(False)
    else:
        weather = weatherDict(options.city)
    # ----OTHER-----------
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
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

                if formA2.exists():
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

                if formA3.exists():
                    most_recent_A3 = formA3[0].date
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
                    A3data = ""
                    lids = ""
                    offtakes = ""

                if formA4.exists():
                    most_recent_A4 = formA4[0].date
                    if most_recent_A4 == today:
                        A4data = formA4[0]
                        form_enteredA4 = True
                    else:
                        A4data = ""
                else:
                    A4data = ""

                if formA5.exists():
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
            if request.method == 'POST':
                answer = request.POST
                print(answer)
                if 'facilitySelect' in answer.keys():
                    if answer['facilitySelect'] != '':
                        return redirect('sup_dashboard', answer['facilitySelect'])
                elif 'colorMode' in answer.keys():
                    print("CHECK 1")
                    colorModeSwitch(request)
                    return redirect(request.META['HTTP_REFERER'])

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
                'colorMode': colorMode,
                'userMode': userMode,
                'notifs': notifs
            })
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard', answer['facilitySelect'])
        elif 'colorMode' in answer.keys():
            print(answer['colorMode'])
            colorModeSwitch(request)
            
        
    return render(request, "supervisor/sup_dashboard.html", {
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
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'sortedFacilityData': sortedFacilityData, 
        'colorMode': colorMode,
        'userMode': userMode,
        'notifs': notifs
    })

@lock
@isSubActive
def register_view(request, facility, access_page):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    options = bat_info_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    user_profiles = user_profile_model.objects.all()
    accountData = user_profiles.get(user__username=request.user.username)
    userCompany = accountData.company
    media = settings.MEDIA_ROOT
    userProfileInfo = ''
    userData2 = ''
    pic = ''
    userInfo = ''
    form = ''
    profile_form = ''
    data = ''
    data2 = bat_info_model.objects.all()
    facilityLink = False
    print(checkIfMoreRegistrations(request.user))
    if checkIfMoreRegistrations(request.user):
        addMoreRegistrations = checkIfMoreRegistrations(request.user)[1]
    else:
        addMoreRegistrations = False

    if supervisor:
        if access_page != 'form' and access_page not in ['client', 'observer', 'facility']:
            if len(user_profiles.filter(user__id__exact=access_page)) > 0:
                userProfileInfo = user_profiles.filter(user__id__exact=access_page)[0]
                userInfo = User.objects.all().filter(id__exact=access_page)[0]
                pic = userProfileInfo.profile_picture
                if userProfileInfo.phone:
                    number = userProfileInfo.phone[2:]
                    first = number[:3]
                    middle = number[3:6]
                    end = number[6:]
                    parseNumber = '(' + first + ')' + middle + '-'+ end
                else:
                    parseNumber = ''
                
                initial_data = {
                    'cert_date': userProfileInfo.cert_date,
                    'phone': parseNumber,
                    'position': userProfileInfo.position,
                    'profile_picture': userProfileInfo.profile_picture,
                    'certs': userProfileInfo.certs,
                    'company': userProfileInfo.company
                }
                userData2 = user_profile_form(initial=initial_data)   
        else:
            form = CreateUserForm()
            profile_form = user_profile_form()
            
            data = bat_info_form()
            
            #"if there are no facilities linked to the request.user's company then we should get back false or "
            userProf = user_profiles.filter(user__username=request.user.username)[0]
            userFacility = options.filter(company=userProf.company)
            if len(userFacility) > 0:
                facilityLink = True
        if request.method == 'POST':
            check_1 = request.POST.get('create_user', False)
            check_2 = request.POST.get('create_facility', False)
            check_3 = request.POST.get('edit_user', False)
            check_4 = request.POST.get('create_client', False)
            if check_1:
                print('CHECK 1')
                finalPhone = '+1' + ''.join(filter(str.isdigit, request.POST['phone']))
                new_data = request.POST.copy()
                new_data['phone'] = finalPhone
                new_data['username'] = request.POST['username'].lower()
                form = CreateUserForm(new_data)
                profile_form = user_profile_form(new_data)
                if form.is_valid() and profile_form.is_valid():
                    user = form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.company = userCompany
                    profile.save()

                    group = Group.objects.get(name=profile.position)
                    user.groups.add(group)

                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)
                    return redirect('sup_dashboard', facility)
                else:
                    messages.error(request, "The Information Entered Was Invalid.")
            elif check_2:
                form = bat_info_form(request.POST)
                profile_form = ''
                if form.is_valid():
                    facilityModel = bat_info_model.objects.filter(facility_name=form['facility_name'])
                    if len(facilityModel) == 0:    
                        A = form.save(commit=False)
                        A.company = userProf.company
                        
                        A.save()
                        
                        messages.success(request, 'Facility Created')
                        return redirect('sup_dashboard', facility)
                    else:
                        print('need error message response for matching Facility names, choose different name')
            elif check_3:
                print('CHECK 3')
                finalPhone = '+1' + ''.join(filter(str.isdigit, request.POST['phone']))
                new_data = request.POST.copy()
                new_data['phone'] = finalPhone
                new_data['company'] = userProfileInfo.company
                A = user_profile_form(new_data, request.FILES, instance=userProfileInfo)
                if A.is_valid():
                    A.save()
                    return redirect('Contacts', facility)
            elif check_4:
                print('CHECK 4')
                facility = bat_info_model.objects.all().filter(id=request.POST['facilityChoice'])[0]
                finalPhone = '+1' + ''.join(filter(str.isdigit, request.POST['phone']))
                new_data = request.POST.copy()
                new_data['phone'] = finalPhone
                new_data['position'] = 'client'
                A = user_profile_form(new_data)
                B = CreateUserForm(new_data)
                if A.is_valid() and B.is_valid():
                    user = B.save()
                    profile = A.save(commit=False)
                    profile.user = user
                    profile.company = userProf.company
                    
                    profile.save()
                    
                    group = Group.objects.get(name=profile.position)
                    user.groups.add(group)

                    user = B.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)

                    return redirect('Contacts', facility)
            else:
                print('TOO FAR')
                
    elif request.user.groups.filter(name=CLIENT_VAR):
        return redirect('c_dashboard')
    elif request.user.groups.filter(name=OBSER_VAR):
        return redirect('IncompleteForms', facility)
    else:
        return redirect('no_registration')
    
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard', answer['facilitySelect'])
    return render(request, "ees_forms/ees_register.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'facilityLink': facilityLink, 
        'userProfileInfo': userProfileInfo, 
        'media': media, 
        'pic': pic, 
        'access_page': access_page, 
        'options': options, 
        'facility': facility, 
        'form': form, 
        'profile_form': profile_form, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'data': data, 
        'data2': data2, 
        'userData2': userData2, 
        'userInfo': userInfo,
        'addMoreRegistrations': addMoreRegistrations
    })
    