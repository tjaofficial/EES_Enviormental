from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth import authenticate, login
import datetime
from ..models import user_profile_model, daily_battery_profile_model, bat_info_model
from ..forms import CreateUserForm, user_profile_form
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

profile = user_profile_model.objects.all()


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
            return redirect('admin_dashboard', 'admin')
        elif request.user.groups.filter(name='SGI Admin'):
            return redirect('admin_dashboard', 'admin')
        elif request.user.groups.filter(name='EES Coke Employees'):
            return redirect('c_dashboard')
        elif request.user.groups.filter(name='SGI Technician'):
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
            if request.user.is_superuser or request.user.groups.filter(name='SGI Admin'):
                if len(bat_info_model.objects.all()) > 0:
                    return redirect('admin_dashboard', 'admin')
                else:
                    return redirect('Register', 'admin', 'facility')
            elif request.user.groups.filter(name='EES Coke Employees'):
                return redirect('c_dashboard')
            elif request.user.groups.filter(name='SGI Technician'):
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
    return render(request, 'landing/landing_register.html',{
        'userForm': userForm, 'profileForm': profileForm
    })