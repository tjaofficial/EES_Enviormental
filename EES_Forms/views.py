from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from .models import *
from .forms import *


daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
todays_log = daily_prof[0]
lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

#------------------------------------------------------------------------REGISTER---------<
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('IncompleteForms')
    else:
        form = CreateUserForm()
        profile_form = user_profile_form()
    
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = user_profile_form(request.POST)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                
                profile = profile_form.save(commit=False)
                profile.user = user
                
                profile.save()
                
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)
                return redirect('Login')
            else:
                messages.error(request, "The Information Entered Was Invalid.")
    return render(request, "ees_forms/ees_register.html", { 
                'form': form, 'profile_form': profile_form
            })
#--------------------------------------------------------------------------------LOGIN---------<
def login_view(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    if request.user.is_authenticated:
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                return redirect('IncompleteForms')  
            else:
                return redirect('daily_battery_profile')
        else:
                return redirect('daily_battery_profile')
        
    else:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                
                
                login(request, user)
                #return redirect('daily_battery_profile')
                
                if now.month == todays_log.date_save.month:
                    if now.day == todays_log.date_save.day:
                        return redirect('IncompleteForms')  
                    else:
                        return redirect('daily_battery_profile')
                else:
                        return redirect('daily_battery_profile')
    return render(request, "ees_forms/ees_login.html", {
         "now": now
    })
#-------------------------------------------------------------------------BATTERY PROFILE---------<
@lock
def daily_battery_profile_view(request):
    
    form = daily_battery_profile_form
    if request.method =='POST':
        form = daily_battery_profile_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('IncompleteForms')
    
    return render (request, "ees_forms/Bat_info.html",{
        'form': form
    })
#----------------------------------------------------------------------------------LOGOUT---------<
def logout_view(request):
    logout(request)
    return redirect ('Login')
#------------------------------------------------------------------------INCOMPLETE FORMS---------<
@lock
def IncompleteForms(request):
    now = datetime.datetime.now()
    pull = Forms.objects.filter(submitted__exact=False).order_by('form')
    pullNot = Forms.objects.filter(submitted__exact=True).order_by('form')
    
    return render(request, "ees_forms/index.html", {
        "pull": pull, "pullNot":pullNot, "now": now, 'todays_log': todays_log, "back": back
    })

#------------------------------------------------------------------ADMIN PUSH TRAVELS-------------<
def pt_admin1_view(request):
    reads = subA5_readings_model.objects.all()
    data = subA5_model.objects.all()
    #add_days = datetime.timedelta(days=91)
    
    
    
    def array_of_dates(reads):
        penis = []
        for item in reads:
            o1 = item.o1
            o2 = item.o2
            o3 = item.o3
            o4 = item.o4
            date = item.form.date
            date_array = date.split("-")
            
            year = int(date_array[0])
            month = int(date_array[1])
            day = int(date_array[2])
            
            form_date = datetime.datetime(year, month, day)
            added_date = form_date + datetime.timedelta(days=91)
            due_date = added_date - datetime.datetime.now() 
            dateObject = {
                'date': date,
                'exp_date': added_date.date,
                'due_date': due_date.days,
                'o1': o1,
                'o2': o2,
                'o3': o3,
                'o4': o4
            }
            penis.append(dateObject)
        return penis
    poop = array_of_dates(reads)
    
   
    return render(request, "ees_forms/PushTravels.html", {
        "now": now, 'todays_log': todays_log, "back": back, 'reads': reads, 'data': data, 'poop': poop
    })
#------------------------------------------------------------------------ADMIN DATA-------------<
@lock
def admin_data_view(request):
    return render (request, "ees_forms/admin_data.html", {
        "back": back, 'todays_log': todays_log 
    })
#------------------------------------------------------------------------A1---------------<
@lock
def formA1(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    full_name = request.user.get_full_name()
    initial_data = {
        'date' : todays_log.date_save,
        'observer' : full_name,
        'crew' : todays_log.crew,
        'foreman' : todays_log.foreman,
    }
    data = subA1_form(initial=initial_data)
    readings = subA1_readings_form()
    #ptadmin = pt_admin1_form()
    if request.method == "POST":
        form = subA1_form(request.POST)
        reads = subA1_readings_form(request.POST)
        #admin = pt_admin1_form(request)
        A_valid = form.is_valid()
        B_valid = form.is_valid()
        #c_valid = admin.is_valid()
        if A_valid and B_valid:# and C_valid:
            A = form.save()
            B = reads.save(commit=False)
            B.form = A
            B.save()
           # D = admin.save(commit=False)
           # D.form = C
            #D.save()
            return redirect('IncompleteForms')
    else:
        form = subA1_form(initial=initial_data)
        readings = subA1_readings_form()
        ptadmin = pt_admin1_form()
    return render (request, "Daily/Method303/formA1.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'readings': readings
    })
#------------------------------------------------------------------------A2---------------<
@lock
def formA2(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    return render (request, "Daily/Method303/formA2.html", {
        "back": back, 'todays_log': todays_log
    })
#------------------------------------------------------------------------A3---------------<
@lock
def formA3(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    return render (request, "Daily/Method303/formA3.html", {
        "back": back, 'todays_log': todays_log
    })
#------------------------------------------------------------------------A4---------------<
@lock
def formA4(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    return render (request, "Daily/Method303/formA4.html", {
        "back": back, 'todays_log': todays_log
    })
#------------------------------------------------------------------------A5---------------<
@lock
def formA5(request):
    this_from = 'A-5'
    
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    initial_data = {
        'date' : todays_log.date_save,
        'estab' : "EES COKE BATTERY",
        'county' : "Wayne",
        'estab_no' : "P0408",
        'equip_loc' : "Zug Island",
        'district' : "Detroit",
        'city' : "River Rouge",
        'observer' : full_name,
        'cert_date' : cert_date,
        'process_equip1' : "Coke Battery / Door Machine / Hot Car",
        'process_equip2' : "Door Machine / PECS",
        'op_mode1' : "normal",
        'op_mode2' : "normal",
        'emission_point_start' : "Above hot car",
        'emission_point_stop' : "Above door machine hood",
        'height_above_ground' : "45",
        'height_rel_observer' : "45",
        'plume_type' : 'N/A', 
        'water_drolet_present' : "No",
        'water_droplet_plume' : "N/A",
        'plume_opacity_determined_start' : "Above hot car",
        'plume_opacity_determined_stop' : "Above door machine hood",
        'describe_background_start' : "Skies",
        'describe_background_stop' : "Same"
    }
    data = subA5_form(initial=initial_data)
    profile_form = user_profile_form()
    readings_form = subA5_readings_form()
    
    if request.method == "POST":
        form = subA5_form(request.POST)
        readings = subA5_readings_form(request.POST)
        A_valid = form.is_valid()
        B_valid = readings.is_valid()
        if A_valid and B_valid:
            A = form.save()
            B = readings.save(commit=False)

            B.form = A
            B.save()
            
            return redirect('IncompleteForms')
    else:
        form = subA5_form(initial=initial_data)
        readings_form = subA5_readings_form()
    return render (request, "Daily/Method303/formA5.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'profile_form': profile_form, 'readings_form': readings_form
    })
#------------------------------------------------------------------------FORM B---------------<
@lock
def formB(request):
    return render (request, "Daily/formB.html", {
        "back": back
    })
#------------------------------------------------------------------------FORM C---------------<
@lock
def formC(request):
    submitted = False
    if request.method == "POST":
        CReadings = FormCReadForm(request.POST)
        CData = SubFormC1(request.POST)
        A_valid = CReadings.is_valid()
        B_valid = CData.is_valid()
        #form.save()
        #return HttpResponseRedirect('./formC?submitted=True')
        if A_valid and B_valid:
            A = CData.save()
            B = CReadings.save(commit=False)
            B.form = A
            B.save()
            return HttpResponseRedirect('./formC?submitted=True')
    else:
        form = SubFormC1
        read = FormCReadForm
        if 'submitted' in request.GET:
            submitted = True
    return render (request, "Daily/formC.html", {
        'form': form, 'read': read, 'submitted': submitted, "back": back, 'now': now
    })

#------------------------------------------------------------------------FORM D---------------<
@lock
def formD(request):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    last_friday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_friday + one_week
    
    week_start_dates = formD_model.objects.all().order_by('-week_start')
    week_almost = week_start_dates[0]
    week = week_almost.week_start
    
    if week == last_friday:
        data = week_almost
        empty_form = formD_form()
        
        if request.method == "POST":
            form = formD_form(request.POST)
            form.save()

            return redirect('IncompleteForms')

    else:
        data = formD_form()
        empty_form = formD_form()
        if request.method == "POST":
            form = formD_form(request.POST)
            form.save()

            return redirect('IncompleteForms')
        
    return render (request, "Daily/formD.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'empty': empty_form, 'week': week, 'last_friday': last_friday, 'week_almost': week_almost, 'end_week': end_week
    })


















































