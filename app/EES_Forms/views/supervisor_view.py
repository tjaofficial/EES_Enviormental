from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.conf import settings # type: ignore
from ..forms import CreateUserForm, user_profile_form, bat_info_form, form_requests_form
from ..models import facility_model, issues_model, form1_model, form2_model, form3_model, Event, form4_model, form5_model, daily_battery_profile_model, User, user_profile_model, facility_forms_model, notifications_model
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
import datetime
import calendar
from django.contrib import messages # type: ignore
from django.contrib.auth.models import Group # type: ignore
import json
from ..utils.main_utils import dashDict, parsePhone, setDefaultSettings, defaultBatteryDashSettings, defaultFacilitySettingsParsed, setUnlockClientSupervisor, weatherDict, calculateProgessBar, ninetyDayPushTravels, colorModeSwitch, userColorMode, checkIfFacilitySelected, getCompanyFacilities, checkIfMoreRegistrations, tryExceptFormDatabases, updateAllFormSubmissions, setUnlockClientSupervisor, defaultBatteryDashSettings, generate_random_string
from ..decor import group_required
from django.core.mail import send_mail # type: ignore
from django.contrib.sites.shortcuts import get_current_site # type: ignore
from django.utils.encoding import force_bytes # type: ignore
from django.utils.http import urlsafe_base64_encode  # type: ignore
from django.template.loader import render_to_string  # type: ignore
from ..tokens import create_token # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.http import JsonResponse # type: ignore

lock = login_required(login_url='Login')

@lock
@group_required(SUPER_VAR)
def sup_dashboard_view(request, facility):
    updateAllFormSubmissions(facility)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    formA1 = form1_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    formA2 = form2_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    formA3 = form3_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    formA4 = form4_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    formA5 = form5_model.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
    fsID1 = tryExceptFormDatabases(1,formA1, facility)
    fsID2 = tryExceptFormDatabases(2,formA2, facility) 
    fsID3 = tryExceptFormDatabases(3,formA3, facility)
    fsID4 = tryExceptFormDatabases(4,formA4, facility)
    fsID5 = tryExceptFormDatabases(5,formA5, facility)
    fsIDs = [fsID1,fsID2,fsID3,fsID4,fsID5]

    now = datetime.datetime.now().date()

    last7days = now - datetime.timedelta(days=6)
    options = facility_model.objects.filter(facility_name=facility)
    emypty_dp_today = True
    colorMode = userColorMode(request.user)[0]  
    userMode = userColorMode(request.user)[1]
    userProfile = request.user.user_profile
    userCompany = userProfile.company
    if options.exists():
        options = options[0]

    today = datetime.date.today()
    #---------- Graph Data ---------------------
    graphData = ''
    graphDataDump = ''
    if facility != SUPER_VAR:
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
                'today': str(today),
                'frequency': setGraphRange, 
            }
            graphDataDump = json.dumps(graphData)
    # -------PROGRESS PERCENTAGES -----------------
    if facility != SUPER_VAR:
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
    if facility != SUPER_VAR:
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
    ca_forms = issues_model.objects.filter(facilityChoice__facility_name=facility).order_by('-id')
    # ----Weather API Pull-----------
    if facility == SUPER_VAR:
        weather = weatherDict(False)
    else:
        weather = weatherDict(options.city)
    # ----OTHER-----------
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
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
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard', answer['facilitySelect'])
        elif 'colorMode' in answer.keys():
            print(answer['colorMode'])
            colorModeSwitch(request)
            
        
    return render(request, "supervisor/sup_dashboard.html", {
        'notifs': notifs,
        'facility': facility, 
        'options': options,
        'userProfile': userProfile
    })

@lock
def header_data(request, facility):
    print("STEP 1")
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    notifSettings = request.user.user_profile.settings['facilities']
    header_data = {
        'facility': facility,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'sortedFacilityData': sortedFacilityData,
        'notifs': notifs,
        'notifSettings': notifSettings,
        'company': request.user.user_profile.company
    }
    return render(request, "supervisor/components/sup_header.html", header_data)

@lock
def get_unread_notification_count(request):
    count = notifications_model.objects.filter(
        user=request.user.user_profile,
        clicked=False,
        hovered=False
    ).count()

    return JsonResponse({'count': count})

@lock
@group_required(SUPER_VAR)
def register_view(request, facility, access_page):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    options = facility_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
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
    data2 = facility_model.objects.all()
    facilityLink = False
    if checkIfMoreRegistrations(request.user):
        addMoreRegistrations = checkIfMoreRegistrations(request.user)[1]
    else:
        addMoreRegistrations = False

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


    if request.method == 'POST':
        check_1 = request.POST.get('create_user', False)
        check_2 = request.POST.get('create_facility', False)
        check_3 = request.POST.get('edit_user', False)
        check_4 = request.POST.get('create_client', False)
        if check_1:
            print('CHECK 1')
            finalPhone = parsePhone(request.POST['phone'])
            new_data = request.POST.copy()
            new_data['phone'] = finalPhone
            new_data['username'] = request.POST['username'].lower()
            randoPass = generate_random_string()
            new_data['password1'] = randoPass
            new_data['password2'] = randoPass
            A = CreateUserForm(new_data)
            B = user_profile_form(new_data)
            print()
            if A.is_valid() and B.is_valid():
                user = A.save(commit=False)
                user.is_active = False
                user.save()
                profile = B.save(commit=False)
                profile.user = user
                profile.company = userCompany
                profile.settings = setDefaultSettings(profile, request.user.username)
                profile.save()

                group = Group.objects.get(name=profile.position)
                user.groups.add(group)

                username = A.cleaned_data.get('username')
                
                current_site = get_current_site(request)
                mail_subject = 'MethodPlus: Activate Your New Account'   
                html_message = render_to_string('email/acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':create_token(user),  
                    'randoPass': randoPass
                })  
                plain_message = strip_tags(html_message)
                to_email = A.cleaned_data.get('email')  
                send_mail(
                    mail_subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [to_email],
                    html_message=html_message,
                    fail_silently=False
                )
                messages.success(request, 'Account was created for ' + username + ". An activation link has been sent to their email.")
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
                facilityModel = facility_model.objects.filter(facility_name=request.POST['facility_name'])
                if not facilityModel.exists():    
                    A = form.save(commit=False)
                    A.company = userProf.company
                    A.settings = defaultFacilitySettingsParsed
                    if request.POST['cokeBattery'] == 'Yes':
                        A.dashboard = 'battery'
                    else:
                        A.dashboard = 'default'
                    A.save()
                    for ups in user_profiles.filter(company=A.company).exclude(position=CLIENT_VAR):
                        if 'dashboard' in ups.settings.keys():
                            if ups.settings['dashboard']:
                                ups.settings['dashboard'][str(A.id)] = dashDict
                            else:
                                ups.settings['dashboard'] = {str(A.id): dashDict}
                        else:
                            print("ERROR")
                        if request.POST['cokeBattery'] == 'Yes':
                            ups.settings['dashboard'][str(A.id)]['batteryDash'] = json.loads(json.dumps(defaultBatteryDashSettings))
                            ups.settings['dashboard'][str(A.id)]['formsDash'] = False
                        ups.save()
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
            finalPhone = parsePhone(request.POST['phone'])
            new_data = request.POST.copy()
            new_data['phone'] = finalPhone
            new_data['company'] = userProfileInfo.company
            A = user_profile_form(new_data, request.FILES, instance=userProfileInfo)
            if A.is_valid():
                A.save()
                return redirect('Contacts', facility)
        elif check_4:
            print('CHECK 4')
            facility = facility_model.objects.filter(id=request.POST['facilityChoice'])[0]
            finalPhone = parsePhone(request.POST['phone'])
            new_data = request.POST.copy()
            new_data['phone'] = finalPhone
            new_data['position'] = 'client'
            randoPass = generate_random_string()
            new_data['password1'] = randoPass
            new_data['password2'] = randoPass
            A = CreateUserForm(new_data)
            B = user_profile_form(new_data)
            if A.is_valid() and B.is_valid():
                user = A.save(commit=False)
                user.is_active = False
                user.save()
                profile = B.save(commit=False)
                profile.user = user
                profile.company = userProf.company
                profile.settings = setDefaultSettings(profile, request.user.username)
                profile.save()
                
                group = Group.objects.get(name=profile.position)
                user.groups.add(group)

                username = A.cleaned_data.get('username')
                
                current_site = get_current_site(request)
                mail_subject = 'MethodPlus: Activate Your New Account'   
                html_message = render_to_string('email/acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':create_token(user),  
                    'randoPass': randoPass
                })  
                plain_message = strip_tags(html_message)
                to_email = A.cleaned_data.get('email')  
                send_mail(
                    mail_subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [to_email],
                    html_message=html_message,
                    fail_silently=False
                )
                messages.success(request, 'Account was created for ' + username + ". An activation link has been sent to their email.")
                return redirect('Contacts', facility)
        else:
            print('TOO FAR')        
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
@group_required(SUPER_VAR)
def form_request_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
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
 