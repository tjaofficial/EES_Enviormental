from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ..forms import CreateUserForm, user_profile_form, bat_info_form, form_requests_form
from ..models import bat_info_model, issues_model, formA1_readings_model, form2_model, form3_model, Event, form4_model, formA5_readings_model, daily_battery_profile_model, User, user_profile_model, facility_forms_model, form1_readings_model
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
import json
from ..utils import setUnlockClientSupervisor, weatherDict, calculateProgessBar, ninetyDayPushTravels, colorModeSwitch, userColorMode, checkIfFacilitySelected, getCompanyFacilities, checkIfMoreRegistrations, tryExceptFormDatabases, userGroupRedirect, updateAllFormSubmissions, setUnlockClientSupervisor2
from ..decor import isSubActive
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode  
from django.template.loader import render_to_string  
from ..tokens import create_token
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

lock = login_required(login_url='Login')

@lock
@isSubActive
def sup_dashboard_view(request, facility):
    permissions = [SUPER_VAR]
    userGroupRedirect(request.user, permissions)
    updateAllFormSubmissions(facility)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor2(request.user)
    formA1 = form1_readings_model.objects.filter(form__facilityChoice__facility_name=facility).order_by('-form')
    formA2 = form2_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    formA3 = form3_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    formA4 = form4_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    formA5 = formA5_readings_model.objects.filter(form__facilityChoice__facility_name=facility).order_by('-form')
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
    colorMode = userColorMode(request.user)[0]  
    userMode = userColorMode(request.user)[1]
    userProfile = user_profile_model.objects.get(user__id=request.user.id)
    userCompany = userProfile.company
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
                if 'facilitySelect' in answer.keys():
                    if answer['facilitySelect'] != '':
                        return redirect('sup_dashboard', answer['facilitySelect'])
                elif 'colorMode' in answer.keys():
                    print("CHECK 1")
                    colorModeSwitch(request)
                    return redirect(request.META['HTTP_REFERER'])

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
                'today': str(now),
                'colorMode': colorMode,
                'userMode': userMode,
            })
    if request.method == 'POST':
        answer = request.POST
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard', answer['facilitySelect'])
        elif 'colorMode' in answer.keys():
            print(answer['colorMode'])
            colorModeSwitch(request)
            
        
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
        'colorMode': colorMode,
        'userMode': userMode,
        'pLeaks': pLeaks,
        'cLeaks': cLeaks
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
    if checkIfMoreRegistrations(request.user):
        addMoreRegistrations = checkIfMoreRegistrations(request.user)[1]
    else:
        addMoreRegistrations = False

    if supervisor:
        print('check 1')
        if access_page != 'form' and access_page not in ['client', 'observer', 'facility']:
            print('check 2')
            if user_profiles.filter(user__id__exact=access_page).exists():
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
            print('check 3')
            form = CreateUserForm()
            profile_form = user_profile_form()
            
            data = bat_info_form()
            
            #"if there are no facilities linked to the request.user's company then we should get back false or "
            userProf = user_profiles.filter(user__username=request.user.username)[0]
            userFacility = options.filter(company=userProf.company)
            if userFacility.exists():
                facilityLink = True
    elif request.user.groups.filter(name=CLIENT_VAR):
        return redirect('c_dashboard')
    elif request.user.groups.filter(name=OBSER_VAR):
        return redirect('IncompleteForms', facility)
    else:
        return redirect('no_registration')


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
            print(request.POST)
            copyRequest = request.POST.copy()
            copyRequest['is_battery'] = request.POST['cokeBattery']
            form = bat_info_form(copyRequest)
            profile_form = ''
            print(form.errors)
            if form.is_valid():
                print(request.POST['facility_name'])
                facilityModel = bat_info_model.objects.filter(facility_name=request.POST['facility_name'])
                if not facilityModel.exists():    
                    A = form.save(commit=False)
                    A.company = userProf.company
                    if request.POST['cokeBattery'] == 'Yes':
                        A.dashboard = 'battery'
                    else:
                        A.dashboard = 'default'
                    
                    A.save()
                    newfacilityForm = facility_forms_model(
                        facilityChoice = A,
                        formData = ''
                    )
                    newfacilityForm.save()
                    
                    messages.success(request, 'Facility Created')
                    return redirect('sup_dashboard', facility)
                else:
                    messages.error(request, "The facility name you have entered is taken, please choose different name")
                    print('need error message response for matching Facility names, choose different name')
                    print(messages)
                    return redirect('Register', facility, 'facility')
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
                
    
    
    # if request.method == 'POST':
    #     answer = request.POST
    #     if 'facilitySelect' in answer.keys():
    #         if answer['facilitySelect'] != '':
    #             return redirect('sup_dashboard', answer['facilitySelect'])
    #     if 'create_facility' in answer.keys():
    #         copyPost = request.POST.copy()
    #         copyPost['position'] = CLIENT_VAR
    #         copyPost['company'] = userCompany
    #         userFrom = CreateUserForm(copyPost)
    #         userProfForm = user_profile_form(copyPost)
    #         print(userFrom.errors)
    #         print(userProfForm.errors)
    #         if len(request.POST['phone']) < 10:
    #             userProfForm.add_error('phone', ValidationError("Please enter a valid phone number. (ie. 1234567890, (123)456-7890)"))
    #             messages.error(request,"Please enter a valid phone number. (ie. 1234567890, (123)456-7890)")
    #         if User.objects.filter(email=request.POST['email']).exists():
    #             userFrom.add_error('email', ValidationError("This email has already been used."))
    #             messages.error(request,"This email has already been used. Please enter a different email.")
    #         if User.objects.filter(username=request.POST['username'].lower()).exists():
    #             userFrom.add_error('username', ValidationError("This username already exists."))
    #             messages.error(request,"This username already exists. Please enter a different username.")
    #         if userFrom.is_valid() and userProfForm.is_valid():
    #             A = userFrom.save(commit=False)
    #             A.is_active = False
    #             A.save()
                
    #             B = userProfForm.save(commit=False)
    #             B.user = A
    #             B.is_active = False
    #             B.save()
                
    #             group = Group.objects.get(name=CLIENT_VAR)
    #             A.groups.add(group)

    #             current_site = get_current_site(request)
    #             mail_subject = 'MethodPlus: Activate Your New Account'   
    #             html_message = render_to_string('email/acc_active_email.html', {  
    #                 'user': A,  
    #                 'domain': current_site.domain,  
    #                 'uid':urlsafe_base64_encode(force_bytes(A.pk)),  
    #                 'token':create_token(A),  
    #             })  
    #             plain_message = strip_tags(html_message)
    #             to_email = userFrom.cleaned_data.get('email')  
    #             send_mail(
    #                 mail_subject,
    #                 plain_message,
    #                 settings.EMAIL_HOST_USER,
    #                 [to_email],
    #                 html_message=html_message,
    #                 fail_silently=False
    #             )
    #             messages.success(request,"Please confirm your email address to complete the registration")
    #             return redirect('Login')
    #         else:
    #             messages.error(request,"Please fix your inputs.")
    #             return redirect('Register', facility, 'client')
                
                
            
    return render(request, "supervisor/register.html", {
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
   
@lock
def form_request_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    sortedFacilityData = getCompanyFacilities(request.user.username)
    form = form_requests_form
    
    if request.method == 'POST':
        answer = request.POST
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard', answer['facilitySelect'])
        else:
            dataCopy = request.POST.copy()
            dataCopy['user'] = request.user
            form = form_requests_form(dataCopy, request.FILES)
            print(form.errors)
            if form.is_valid():
                A = form.save(commit=False)
                A.form_example_url = A.form_example_file.url
                A.user = request.user
                A.save()
                print('SAVED IT')
                messages.success(request, 'Your request has been submitted. MethodPlus will contact you within 1-2 business days.')
                return redirect('sup_dashboard', 'supervisor')
    return render(request, 'supervisor/request_form.html', {
        'facility': facility,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'form': form
    })   
 