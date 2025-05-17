from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.conf import settings # type: ignore
from ..forms import CreateUserForm, user_profile_form, bat_info_form, form_requests_form
from ..models import facility_model, User, user_profile_model, facility_forms_model, notifications_model
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
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
def sup_dashboard_view(request):
    facility = getattr(request, 'facility', None)
    # if not facility:
    #     return redirect('select_facility_page')  # or handle default
    updateAllFormSubmissions(facility)
    colorMode = userColorMode(request.user)[0]  
    userMode = userColorMode(request.user)[1]

    if request.method == 'POST':
        answer = request.POST
        if 'colorMode' in answer.keys():
            print("CHECK 1")
            print(answer['colorMode'])
            colorModeSwitch(request)    
            return redirect(request.META['HTTP_REFERER'])
        
    return render(request, "supervisor/sup_dashboard.html", {
        'facility': facility,
        'colorMode': colorMode,
        'userMode': userMode,
    })

@lock
def header_data(request):
    print("STEP 1")
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    notifSettings = request.user.user_profile.settings['facilities']
    header_data = {
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
def register_view(request, access_page):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
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
                if 'username' in form.errors:
                    messages.error(request, form.errors['username'][0])
                elif 'email' in form.errors:
                    messages.error(request,"This email has already been used. Please enter a different email.")
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
                return redirect('Contacts')
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
def form_request_view(request):
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    form = form_requests_form
    
    if request.method == 'POST':
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
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'form': form
    })   
 