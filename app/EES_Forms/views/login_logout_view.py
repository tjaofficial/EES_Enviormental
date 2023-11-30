from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import datetime
from ..models import user_profile_model, daily_battery_profile_model, bat_info_model, company_model, braintree_model
from ..forms import CreateUserForm, user_profile_form, company_form, braintree_form
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import Group
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

profile = user_profile_model.objects.all()
lock = login_required(login_url='Login')

def login_view(request):
    loginPage = True
    facility = ''
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    count_bp = daily_battery_profile_model.objects.count()
    existing = False
    login_error = {"error":False, "message":''}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminDash')
        elif request.user.groups.filter(name=SUPER_VAR):
            return redirect('sup_dashboard', SUPER_VAR)
        elif request.user.groups.filter(name=CLIENT_VAR):
            facility = user_profile_model.objects.all().filter(user__username=request.user.username)[0].facilityChoice.facility_name
            return redirect('c_dashboard', facility)
        elif request.user.groups.filter(name=OBSER_VAR):
            if count_bp != 0:
                todays_log = daily_prof[0]
                if now.month == todays_log.date_save.month:
                    if now.day == todays_log.date_save.day:
                        return redirect('facilitySelect')
                batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof) 
        else:
            return redirect('no_registration')
        access = False
    else:
        access = True

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username.lower(), password=password)
        
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('adminDash')
            elif request.user.groups.filter(name=SUPER_VAR):
                if len(bat_info_model.objects.all()) > 0:
                    return redirect('sup_dashboard', SUPER_VAR)
                else:
                    return redirect('Register', SUPER_VAR, 'facility')
            elif request.user.groups.filter(name=CLIENT_VAR):
                facility = user_profile_model.objects.all().filter(user__username=request.user.username)[0].facilityChoice.facility_name
                return redirect('c_dashboard', facility)
            elif request.user.groups.filter(name=OBSER_VAR):
                return redirect('facilitySelect')
                # if count_bp != 0:
                #     todays_log = daily_prof[0]
                #     if now.month == todays_log.date_save.month:
                #         if now.day == todays_log.date_save.day:
                #             return redirect('IncompleteForms')
                # else:
                #     return HttpResponseNotFound("No Battry Profile Data In Data Base")
                
                #batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            else:
                return HttpResponseNotFound("None of the Users in database are assigned a group")
        
        else:
            login_error["error"] = True
            login_error["message"] = 'Incorrect username or password'

    return render(request, "ees_forms/ees_login.html", {
        'facility': facility, "now": now, "login_error": login_error, 'access': access, 'loginPage': loginPage
    })

def valid_account_logout(request):
    
    return render(request, "admin/no_registration.html")
    
def logout_view(request):
    logout(request)

    return redirect('Login')


def profile_redirect(request, facility):
    return redirect('../' + facility + '/profile/main')

    return render(request, 'profile.hmtl', {

    })

def change_password(request, facility):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('profile_redirect', facility)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ees_forms/ees_password.html', {
        'form': form, 'facility': facility
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
        if form.is_valid()and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            
            group = Group.objects.get(name=SUPER_VAR)
            user.groups.add(group)

            user = form.cleaned_data.get('username')
            
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            messages.success(request, 'Account was created for ' + user)
            return redirect('companyReg')
    return render(request, 'landing/landing_register.html',{
        'userForm': userForm, 'profileForm': profileForm
    })
    
@lock    
def registerCompany(request):
    userProf = user_profile_model.objects.filter(user__id=request.user.id)[0]
    companyForm = company_form()
    print(userProf.company)
    if request.method == 'POST':
        finalPhone = '+1' + ''.join(filter(str.isdigit, request.POST['phone']))
        new_data = request.POST.copy()
        new_data['phone'] = finalPhone
        form = company_form(new_data)
        form2 = braintree_form(new_data)
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
                    braintreeSave = braintree_model(user=request.user, status='inactive', registrations=0)
                    braintreeSave.save()
                companySave = form.save(commit=False)
                companySave.braintree = braintreeSave
                companySave.save()
                userProf.company = companySave
                braintreeSave.save()
                companySave.save()
                userProf.save()

                return redirect('billing', 'subscriptions')
    return render(request, 'landing/registerCompany.html',{
        'companyForm': companyForm,
    })