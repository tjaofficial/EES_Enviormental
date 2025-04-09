from django.shortcuts import render, redirect # type: ignore
from django.http import HttpResponseNotFound, HttpResponse # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
import datetime
import json
from ..models import user_profile_model, daily_battery_profile_model, bat_info_model, company_model, braintree_model, User
from ..forms import CreateUserForm, user_profile_form, company_form, braintree_form
from ..utils import parsePhone, setDefaultSettings, setUnlockClientSupervisor
from django.contrib.auth import logout # type: ignore
from django.contrib.auth.forms import PasswordChangeForm # type: ignore
from django.contrib.auth import update_session_auth_hash, get_user_model # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.models import Group # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR, EMAIL_HOST_USER
from django.core.mail import send_mail # type: ignore
from django.contrib.sites.shortcuts import get_current_site # type: ignore
from django.utils.encoding import force_bytes, force_str # type: ignore
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # type: ignore
from django.template.loader import render_to_string # type: ignore
from ..tokens import create_token, check_token, delete_token
from django.conf import settings # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.core.exceptions import ValidationError # type: ignore


profile = user_profile_model.objects.all()
lock = login_required(login_url='Login')

def login_view(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now().date()
    count_bp = daily_battery_profile_model.objects.count()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminDash', "overview")
        elif request.user.groups.filter(name=SUPER_VAR):
            return redirect('sup_dashboard', SUPER_VAR)
        elif request.user.groups.filter(name=CLIENT_VAR):
            facility = user_profile_model.objects.all().filter(user__username=request.user.username)[0].facilityChoice.facility_name
            return redirect('c_dashboard', facility)
        elif request.user.groups.filter(name=OBSER_VAR):
            return redirect('facilitySelect', OBSER_VAR)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username.lower(), password=password)
        
        if user is not None:
            login(request, user)
            print('check 1')
            userProf = user_profile_model.objects.filter(user__id=request.user.id)
            if request.user.is_superuser:
                return redirect('adminDash', "overview")
            elif userProf.exists():
                userProf = userProf[0]
                if not userProf.company and userProf.is_active:
                    return redirect('companyReg')
                if request.user.groups.filter(name=SUPER_VAR):
                    if userProf.settings['first_login']:
                        if len(bat_info_model.objects.all()) > 0:
                            return redirect('sup_dashboard', SUPER_VAR)
                        else:
                            return redirect('Register', SUPER_VAR, 'facility')
                    else:
                        return redirect('PasswordChange', SUPER_VAR)
                elif request.user.groups.filter(name=CLIENT_VAR):
                    facility = user_profile_model.objects.all().filter(user__username=request.user.username)[0].facilityChoice.facility_name
                    if userProf.settings['first_login']:
                        return redirect('c_dashboard', facility)
                    else:
                        return redirect('PasswordChange', facility)
                elif request.user.groups.filter(name=OBSER_VAR):
                    if userProf.settings['first_login']:
                        return redirect('facilitySelect', 'observer')
                    else:
                        return redirect('PasswordChange', OBSER_VAR)
                else:
                    messages.error(request,"User has not been assigned a group. Please contact MethodPlus help for further assistance.")
                    return redirect('Login')
            else:
                messages.error(request,"ERROR: ID-11850004. Contact Support Team.")
                return redirect('Login')
        else:
            messages.error(request,"Incorrect username or password")
            return redirect('Login')
    return render(request, "shared/login.html", {})
    
def logout_view(request):
    logout(request)

    return redirect('Login')

def activate_view(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)
        userProf = user_profile_model.objects.get(user=user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and check_token(user, token):
        A = user
        B = userProf
        A.is_active = True  
        B.is_active = True
        A.save()
        B.save()
        delete_token(user, token)

        messages.success(request, 'Account has been activated. Please Login for further instruction.')
        return redirect('Login')
    else:  
        messages.success(request, 'Your account has already been activated. Please Login for further instruction.')
        return redirect('Login')
        # return HttpResponse('Activation link is invalid!') 
    
def reset_password_activate_view(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and check_token(user, token):  
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if new_password != confirm_password:
                messages.success(request, 'Your passwords do not match.')
                return redirect('reset', uidb64, token) 
            user.set_password(new_password)
            user.save()
            delete_token(user, token)
            messages.success(request, 'Your password was successfully updated. Please login.')
            return redirect('Login')
        return render(request, 'landing/landing_resetPasswordChange.html', {})
    else:
        messages.success(request, 'No user found/Invalid Activation link. Try Again.')
        return redirect('Login') 

def request_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if user.exists():
            if len(user) == 1:
                user = user[0]
                userProfile = user_profile_model.objects.get(user=user)
                if userProfile.is_active:
                    mail_subject = 'MethodPlus: Reset Your Account Password'   
                    current_site = get_current_site(request)
                    html_message = render_to_string('email/reset_password_email.html', {  
                        'user': user,  
                        'domain': current_site.domain,  
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                        'token':create_token(user),  
                    })
                    plain_message = strip_tags(html_message)
                    to_email = email 
                    send_mail(
                        mail_subject,
                        plain_message,
                        EMAIL_HOST_USER,
                        [to_email],
                        html_message=html_message,
                        fail_silently=False
                    )
                    messages.success(request,"Please check you email. If there is an account registered to that email, we will send you instructions to reset your password.")
                    return redirect('Login')
                else:
                    print('Not an active profile')
            else:
                print('Multiple users with email')
        else:
            print('User does not exist')
            
        
    return render(request, 'landing/landing_requestPasswordChange.html', {
    })

def main_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile', 'main')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'landing/landing_passwordChange.html', {
        'form': form
    })
    
def change_password(request, facility):
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            userProf = user_profile_model.objects.get(user=request.user)
            if not userProf.settings['first_login']:
                userProf.settings['first_login'] = True
                userProf.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('Account', facility)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ees_forms/ees_password.html', {
        'form': form, 
        'facility': facility,
        'unlock': unlock,
        'supervisor': supervisor, 
        "client": client, 
    })

def landingRegister(request):
    userForm = CreateUserForm()
    profileForm = user_profile_form()
    
    if request.method == 'POST':
        finalPhone = '+1' + ''.join(filter(str.isdigit, request.POST['phone']))
        new_data = request.POST.copy()
        new_data['phone'] = finalPhone
        new_data['username'] = request.POST['username'].lower()
        new_data['position'] = SUPER_VAR
        form = CreateUserForm(new_data)
        profile_form = user_profile_form(new_data)
        print(len(request.POST['phone']))
        if len(request.POST['phone']) < 10:
            profile_form.add_error('phone', ValidationError("Please enter a valid phone number. (ie. 1234567890, (123)456-7890)"))
            messages.error(request,"Please enter a valid phone number. (ie. 1234567890, (123)456-7890)")
        if User.objects.filter(email=request.POST['email']).exists():
            form.add_error('email', ValidationError("This email has already been used."))
            messages.error(request,"This email has already been used. Please enter a different email.")
        if User.objects.filter(username=request.POST['username'].lower()).exists():
            form.add_error('username', ValidationError("This username already exists."))
            messages.error(request,"This username already exists. Please enter a different username.")
        print(profile_form.errors)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_active = False
            profile.settings = setDefaultSettings(profile, user.username)
            profile.settings['first_login'] = True
            profile.settings['position'] = SUPER_VAR + "-m"
            
            profile.save()
            
            group = Group.objects.get(name=SUPER_VAR)
            user.groups.add(group)

            current_site = get_current_site(request)
            mail_subject = 'MethodPlus: Activate Your New Account'   
            html_message = render_to_string('email/landing_acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':create_token(user),  
            })  
            plain_message = strip_tags(html_message)
            to_email = form.cleaned_data.get('email')  
            send_mail(
                mail_subject,
                plain_message,
                EMAIL_HOST_USER,
                [to_email],
                html_message=html_message,
                fail_silently=False
            )
            messages.success(request,"Please confirm your email address to complete the registration")
            return redirect('Login')
        else:
            messages.error(request,"Please fix your inputs.")
            return redirect('register')
    return render(request, 'landing/landing_register.html',{
        'userForm': userForm, 'profileForm': profileForm
    })
    
@lock    
def registerCompany(request):
    userProf = user_profile_model.objects.filter(user__id=request.user.id)[0]
    companyForm = company_form()
    print(userProf.company)
    if request.method == 'POST':
        finalPhone = parsePhone(request.POST['phone'])
        new_data = request.POST.copy()
        new_data['phone'] = finalPhone
        form = company_form(new_data)
        form2 = braintree_form(new_data)
        if company_model.objects.filter(company_name=request.POST['company_name']).exists():
            form.add_error('company_name', ValidationError("This Company already exists. Please choose a different company name or contact out Support Team."))
            messages.error(request,"This Company already exists. Please choose a different company name or contact out Support Team.")
        if form.is_valid():
            companyNameCheck = company_model.objects.filter(company_name=request.POST['company_name'])
            if companyNameCheck.exists():
                print('CREATE PAGE TO SHOW POSSIBLE COMPANIES')
            else:
                print('Did not find duplciates in dataBase, ')
                braintreeQuery = braintree_model.objects.filter(user__id=request.user.id)
                if braintreeQuery.exists():
                    braintreeSave = braintreeQuery[0]
                else:
                    braintreeSave = braintree_model(
                        user=request.user,
                        settings = json.loads(json.dumps({"account": {"status": "inactive", "customer_ID": False}, "subscription": False, "payment_methods": False}))
                    )
                    braintreeSave.save()
                companySave = form.save(commit=False)
                companySave.braintree = braintreeSave
                companySave.save()
                userProf.company = companySave
                braintreeSave.save()
                companySave.save()
                userProf.save()

                return redirect('billing', 'subscription')
    return render(request, 'landing/registerCompany.html',{
        'companyForm': companyForm,
    })