from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from operator import itemgetter
import datetime
import calendar
from calendar import HTMLCalendar
from .models import *
from .forms import *
from .utils import DBEmpty, EventCalendar, Calendar
from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist, FieldError
import requests
from django.contrib.auth.models import User, Group




daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
todays_log = daily_prof[0]
lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')
sub_forms = Forms.objects.all()
today = datetime.date.today()
now = datetime.datetime.now()
profile = user_profile_model.objects.all()

    

#--------------------------------------------------------------------------REGISTER---------<
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
                batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
                
                return redirect(batt_prof)
        else:
            batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
                
            return redirect(batt_prof)
        
    else:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
                if now.month == todays_log.date_save.month:
                    if now.day == todays_log.date_save.day:
                        return redirect('IncompleteForms')  
                    else:
                        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
                
                        return redirect(batt_prof)
                else:
                    batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
                
                    return redirect(batt_prof)
                    
                    
    return render(request, "ees_forms/ees_login.html", {
         "now": now
    })
#-------------------------------------------------------------------------BATTERY PROFILE---------<
@lock
def daily_battery_profile_view(request, access_page, date):
    profile = user_profile_model.objects.all()
    form = daily_battery_profile_form
    
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    if now.month == todays_log.date_save.month:
        if now.day == todays_log.date_save.day:
            initial_data = {
                'foreman' : todays_log.foreman,
                'crew' : todays_log.crew,
                'inop_ovens' : todays_log.inop_ovens,
                'date_save' : todays_log.date_save,
            }
            form = daily_battery_profile_form(initial=initial_data)
            
            if request.method =='POST':
                form = daily_battery_profile_form(request.POST, instance= todays_log)
                if form.is_valid():
                    form.save()
                    
                    return redirect('IncompleteForms')
        else:
            if request.method =='POST':
                form = daily_battery_profile_form(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('IncompleteForms')
    else:
        if request.method =='POST':
            form = daily_battery_profile_form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('IncompleteForms')
    
    return render (request, "ees_forms/Bat_Info.html",{
        'form': form, 'now': now, 'todays_log': todays_log, 'profile':profile, 
    })
#----------------------------------------------------------------------------------LOGOUT---------<
def logout_view(request):
    logout(request)
    return redirect ('Login')
#------------------------------------------------------------------------INCOMPLETE FORMS---------<
@lock
def IncompleteForms(request):
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser or request.user.groups.filter(name='SGI Quality Control'):
    
        profile = user_profile_model.objects.all()
        today = datetime.date.today()
        todays_num = today.weekday()
        sub_forms = Forms.objects.all()
        reads = formA5_readings_model.objects.all()
        today_str = str(today)

        weekday_fri = today + datetime.timedelta(days= 4 - todays_num)
        weekend_fri = weekday_fri + datetime.timedelta(days=7)


    #-ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
    #-ADD IN THE FORMS IF DATABASE HAS LESS THAN 5----------
        if Forms.objects.count() <= 5:
            A1 = Forms(
                form="A-1", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formA1", 
                header="Method 303",
                title="Charging", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            A2 = Forms(
                form="A-2", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formA2", 
                header="Method 303",
                title="Doors", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            A3 = Forms(
                form="A-3", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formA3", 
                header="Method 303",
                title="Lids and Offtakes", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            A4 = Forms(
                form="A-4", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formA4", 
                header="Method 303",
                title="Collection Main", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            A5 = Forms(
                form="A-5", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formA5", 
                header="Method 9B",
                title="Push Travels", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            B = Forms(
                form="B", 
                frequency="Daily",
                day_freq = 'Any',
                weekdays_only = True,
                weekend_only = False,
                link="formB", 
                header="Method 9",
                title="Fugitive Dust Inspection", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            C = Forms(
                form="C", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formC", 
                header="Method 9",
                title="Method 9D - Coal Field", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            D = Forms(
                form="D", 
                frequency="Weekly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formD", 
                header="Method 9",
                title="Random Truck Inspection", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            E = Forms(
                form="E", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formE", 
                header="Method 9",
                title="Gooseneck Inspection", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            F1 = Forms(
                form="F-1", 
                frequency="Weekly", 
                day_freq = 'Wednesday',
                weekdays_only = False,
                weekend_only = False,
                link="formF1", 
                header="Waste Weekly Inspections",
                title="SIF / K087 Process Area (Satellite)", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            F2 = Forms(
                form="F-2", 
                frequency="Weekly", 
                day_freq = 'Wednesday',
                weekdays_only = False,
                weekend_only = False,
                link="formF2", 
                header="Waste Weekly Inspections",
                title="#1 Shop (Satellite Accumulation)", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            F3 = Forms(
                form="F-3", 
                frequency="Weekly", 
                day_freq = 'Wednesday',
                weekdays_only = False,
                weekend_only = False,
                link="formF3", 
                header="Waste Weekly Inspections",
                title="#2 Shop (Satellite Accumulation)", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            F4 = Forms(
                form="F-4", 
                frequency="Weekly", 
                day_freq = 'Wednesday',
                weekdays_only = False,
                weekend_only = False,
                link="formF4", 
                header="Waste Weekly Inspections",
                title="Battery (Satellite Accumulation)", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            F5 = Forms(
                form="F-5", 
                frequency="Weekly", 
                day_freq = 'Wednesday',
                weekdays_only = False,
                weekend_only = False,
                link="formF5", 
                header="Waste Weekly Inspections",
                title="Bio Plant (Satellite Accumulation)", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            F6 = Forms(
                form="F-6", 
                frequency="Weekly", 
                day_freq = 'Wednesday',
                weekdays_only = False,
                weekend_only = False,
                link="formF6", 
                header="Waste Weekly Inspections",
                title="No. 8 Tank Area (Satellite Accumulation)", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            F7 = Forms(
                form="F-7", 
                frequency="Weekly", 
                day_freq = 'Wednesday',
                weekdays_only = False,
                weekend_only = False,
                link="formF7", 
                header="Waste Weekly Inspections",
                title="Booster Pad (90-Day Accumulation)", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            G1 = Forms(
                form="G-1", 
                frequency="Weekly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formG1", 
                header="PECS Baghouse Stack",
                title="Method 9/Non-Certified Observations", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            G2 = Forms(
                form="G-2", 
                frequency="Weekly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formG2", 
                header="PECS Baghouse Stack",
                title="Method 9B", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            H = Forms(
                form="H", 
                frequency="Weekly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formH", 
                header="Method 9",
                title="Method 9 - Combustion Stack", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            I = Forms(
                form="I", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = True,
                weekend_only = False,
                link="formI", 
                header="Sampling",
                title="Quench Water Sampling Form", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            L = Forms(
                form="L", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = True,
                weekend_only = False,
                link="formL", 
                header="Method 9",
                title="Visual Emissions Observations", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            M = Forms(
                form="M", 
                frequency="Daily", 
                day_freq = 'Any',
                weekdays_only = True,
                weekend_only = False,
                link="formM", 
                header="Method 9D",
                title="Method 9D Observation", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            N = Forms(
                form="N", 
                frequency="Monthly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="formN", 
                header="Fugitive Dust Inspection",
                title="Method 9D Monthly Checklist", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            O = Forms(
                form="O", 
                frequency="Weekly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = True,
                link="formO", 
                header="Stormwater Observation Form",
                title="MP 108A", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            P = Forms(
                form="P", 
                frequency="Weekly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = True,
                link="formP", 
                header="Outfall Observation Form",
                title="Outfall 008", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            spill_kits = Forms(
                form="spill_kits", 
                frequency="Monthly", 
                day_freq = 'Any',
                weekdays_only = False,
                weekend_only = False,
                link="spill_kits", 
                header="Spill Kits Form",
                title="Inspection Check List", 
                due_date=today, 
                date_submitted= today - datetime.timedelta(days=1), 
                submitted= False,)
            
            A1.save()
            A2.save()
            A3.save()
            A4.save()
            A5.save()
            B.save()
            C.save()
            D.save()
            E.save()
            F1.save()
            F2.save()
            F3.save()
            F4.save()
            F5.save()
            F6.save()
            F7.save()
            G1.save()
            G2.save()
            H.save()
            I.save()
            L.save()
            M.save()
            N.save()
            O.save()
            P.save()
            spill_kits.save()
            
            



    #--------------------------------------------Closest Oven Due-----------------    
    #--------------------------------------------Closest Oven Due-----------------       
    #--------------------------------------------Closest Oven Due-----------------    







        def all_ovens(reads):
            A = []
            for items in reads:
                date = items.form.date
              #  date_array = date.split("-")

                year = date.year
                month = date.month
                day = date.day

                form_date = datetime.datetime(year, month, day)
                added_date = form_date + datetime.timedelta(days=91)
                due_date = added_date - datetime.datetime.now() 

                if len(str(items.o1)) == 1 :
                    oven1 = "0" + str(items.o1)
                else:
                    oven1 = items.o1
                A.append((oven1, items.form.date, added_date.date, due_date.days)) 

                if len(str(items.o2)) == 1 :
                    oven2 = "0" + str(items.o2)
                else:
                    oven2 = items.o2
                A.append((oven2, items.form.date, added_date.date, due_date.days))

                if len(str(items.o3)) == 1 :
                    oven3 = "0" + str(items.o3)
                else:
                    oven3 = items.o3
                A.append((oven3, items.form.date, added_date.date, due_date.days))    

                if len(str(items.o4)) == 1 :
                    oven4 = "0" + str(items.o4)
                else:
                    oven4 = items.o4
                A.append((oven4, items.form.date, added_date.date, due_date.days))      

            return A   

        hello = all_ovens(reads)
        func = lambda x: (x[0], x[1])
        sort = sorted(hello, key = func, reverse=True)
       # print (sort)

        def final(sort):
            B = []
            i = 1
            for new in sort:
                B.append(new)

            for x in sort:
                for y in range(i, len(sort)):
                    tree = sort[y]
                    if tree[0] == x[0]:
                        if tree in B:
                            B.remove(tree)
                i+=1
            return B
        cool = final(sort)

        def overdue_closest(cool):
            F = []

            func2 = lambda R: (R[3])  
            sort2 = sorted(cool, key = func2)
            most_recent = sort2[0][3]

            for x in sort2:
                if x[3] == most_recent:
                    F.append(x)
            return F

        od_recent = overdue_closest(cool)








    #--------------------------------------------Battery Profile Data------------    
    #--------------------------------------------Battery Profile Data------------    
    #--------------------------------------------Battery Profile Data------------    
        daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
        todays_log = daily_prof[0]

        profile_entered = False
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                profile_entered = True

     #------------------------------------------------------Weather-------------    
    #------------------------------------------------------Weather-------------    
    #------------------------------------------------------Weather-------------       


        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'

        city = 'Dearborn'

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'wind_speed' : city_weather['wind']['speed'],
            'wind_direction' : city_weather['wind']['deg'],
            'humidity' : city_weather['main']['humidity'],
        }

        degree = weather['wind_direction']


        def toTextualDescription(degree):
            if degree > 337.5:
                return 'N'
            if degree > 292.5:
                return 'NW'
            if degree > 247.5:
                return 'W'
            if degree > 202.5:
                return 'SW'
            if degree > 157.5:
                return 'S'
            if degree > 122.5:
                return 'SE'
            if degree > 67.5:
                return 'E'
            if degree > 22.5:
                return 'NE'
            return 'N'

        wind_direction = toTextualDescription(degree)






    #------------------------------------------------------Form Data-------------    
    #------------------------------------------------------Form Data-------------    
    #------------------------------------------------------Form Data-------------    
        for forms in sub_forms:
            if todays_num in {0, 1, 2, 3 , 4}:
                forms.due_date = weekday_fri

                A = forms.date_submitted
                if today != A :
                    forms.submitted = False
                    forms.save()
            else:
                forms.due_date = weekend_fri
                
                A = forms.date_submitted
                if today != A :
                    forms.submitted = False
                    forms.save()


        pull = Forms.objects.filter(submitted__exact=False).order_by('form')
        pullNot = Forms.objects.filter(submitted__exact=True).order_by('form')

        day_number = today.weekday()

        if day_number == 6:
            saturday = False
        else:
            saturday = True

        weekend_list = [5,6]
        form_check1 = ["",]
        form_check2 = ["",]
    
    else:
        poop = User.objects.all().order_by('id')
        print(poop[1].groups.all())
        for a in poop:
            print(a)
            print(a.groups.all())
            print('')
            q_group = a.groups.all()
            for x in q_group:
                print(x)
                if str(x) == 'EES Coke Employees':
                    print(a)
                    print(x)
                    return redirect ('c_dashboard')
    
    return render(request, "ees_forms/dashboard.html", {
        "pull": pull, "pullNot":pullNot, "today": today, 'od_recent': od_recent, "todays_log": todays_log, 'now':now, 'profile_entered': profile_entered, 'form_check1': form_check1, 'form_check2': form_check2, 'profile':profile, 'today_str':today_str, 'todays_num': todays_num, 'day_number': day_number, 'weekend_list': weekend_list, 'weather': weather, 'wind_direction': wind_direction, 'saturday': saturday,
    })

def weekly_forms(request):
    pull = Forms.objects.filter(submitted__exact=False).order_by('form')
    pullNot = Forms.objects.filter(submitted__exact=True).order_by('form')
    
    form_incomplete = []
    for x in pull:
        if x.form in {"D", "G-1", "H"}:
            form_incomplete.append(x)
            
    form_complete = []
    for s in pullNot:
        if s.form in {"D", "G-1", "H"}:
            form_complete.append(s)
    
    
    return render(request, "ees_forms/dashboard.html", {
        "pull": pull, "pullNot":pullNot, "today": today, 'form_incomplete': form_incomplete, 'form_complete': form_complete #'todays_log': todays_log, "back": back, 'sub_forms':sub_forms
    })
#------------------------------------------------------------ADMIN PUSH TRAVELS-------------<
def pt_admin1_view(request):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    reads = formA5_readings_model.objects.all()
    data = formA5_model.objects.all()
    #add_days = datetime.timedelta(days=91)
    
    def all_ovens(reads):
        A = []
        for items in reads:
            date = items.form.date
          #  date_array = date.split("-")
            
            year = date.year
            month = date.month
            day = date.day
            
            form_date = datetime.datetime(year, month, day)
            added_date = form_date + datetime.timedelta(days=91)
            due_date = added_date - datetime.datetime.now() 
            
            if len(str(items.o1)) == 1 :
                oven1 = "0" + str(items.o1)
            else:
                oven1 = items.o1
            A.append((oven1, items.form.date, added_date.date, due_date.days)) 
            
            if len(str(items.o2)) == 1 :
                oven2 = "0" + str(items.o2)
            else:
                oven2 = items.o2
            A.append((oven2, items.form.date, added_date.date, due_date.days))
                
            if len(str(items.o3)) == 1 :
                oven3 = "0" + str(items.o3)
            else:
                oven3 = items.o3
            A.append((oven3, items.form.date, added_date.date, due_date.days))    
                
            if len(str(items.o4)) == 1 :
                oven4 = "0" + str(items.o4)
            else:
                oven4 = items.o4
            A.append((oven4, items.form.date, added_date.date, due_date.days))      

        return A   
    
    hello = all_ovens(reads)
    func = lambda x: (x[0], x[1])
    sort = sorted(hello, key = func, reverse=True)
   # print (sort)
    
    def final(sort):
        B = []
        i = 1
        for new in sort:
            B.append(new)
        
        for x in sort:
            for y in range(i, len(sort)):
                tree = sort[y]
                if tree[0] == x[0]:
                    if tree in B:
                        B.remove(tree)
            i+=1
        return B
    cool = final(sort)
    
    def overdue_30(cool):
        C = []
        for x in cool:
            if x[3] <= 30 :
                C.append(x)
        return C
    
    def overdue_10(cool):
        D = []
        for x in cool:
            if x[3] <= 10 :
                D.append(x)
        return D
    
    def overdue_5(cool):
        E = []
        for x in cool:
            if x[3] <= 5 :
                E.append(x)
        return E
    
    def overdue_closest(cool):
        F = []
        
        func2 = lambda R: (R[3])  
        sort2 = sorted(cool, key = func2)
        most_recent = sort2[0][3]
        
        for x in sort2:
            if x[3] == most_recent:
                F.append(x)
        return F
    
    od_30 = overdue_30(cool)
    od_10 = overdue_10(cool)
    od_5 = overdue_5(cool)
    od_recent = overdue_closest(cool)
    
    return render(request, "ees_forms/PushTravels.html", {
        "now": now, 'todays_log': todays_log, "back": back, 'reads': reads, 'data': data, 'cool': cool, 'od_30': od_30, 'od_10': od_10, 'od_5': od_5, 'od_recent': od_recent, "today": today, 'profile':profile, 'client': client,
    })
#------------------------------------------------------------------------ADMIN DATA-------------<


def pt_mth_input(request):
    submitted_ordered = formA5_readings_model.objects.all()
    
    def pt_sort(submitted_ordered):
        A = []
        for x in submitted_ordered:
            date = x.form.date
            i = 1
            h = i+1
            j = i+2
            k = i+4
            A.append((
                date,
                x.o1,
                x.o1_start, 
                x.o1_1_reads,
                x.o1_2_reads,
                x.o1_3_reads,
                x.o1_4_reads,
                x.o1_5_reads,
                x.o1_6_reads,
                x.o1_7_reads,
                x.o1_8_reads,
                x.o1_9_reads,
                x.o1_10_reads,
                x.o1_11_reads,
                x.o1_12_reads,
                x.o1_13_reads,
                x.o1_14_reads,
                x.o1_15_reads,
                x.o1_16_reads,
                'lightblue',
                i
            ))
            A.append((
                date, 
                x.o2,
                x.o2_start, 
                x.o2_1_reads,
                x.o2_2_reads,
                x.o2_3_reads,
                x.o2_4_reads,
                x.o2_5_reads,
                x.o2_6_reads,
                x.o2_7_reads,
                x.o2_8_reads,
                x.o2_9_reads,
                x.o2_10_reads,
                x.o2_11_reads,
                x.o2_12_reads,
                x.o2_13_reads,
                x.o2_14_reads,
                x.o2_15_reads,
                x.o2_16_reads,
                'skyblue',
                h
            ))
            A.append((
                date, 
                x.o3,
                x.o3_start, 
                x.o3_1_reads,
                x.o3_2_reads,
                x.o3_3_reads,
                x.o3_4_reads,
                x.o3_5_reads,
                x.o3_6_reads,
                x.o3_7_reads,
                x.o3_8_reads,
                x.o3_9_reads,
                x.o3_10_reads,
                x.o3_11_reads,
                x.o3_12_reads,
                x.o3_13_reads,
                x.o3_14_reads,
                x.o3_15_reads,
                x.o3_16_reads,
                'lightblue',
                j
            ))
            A.append((
                date, 
                x.o4,
                x.o4_start, 
                x.o4_1_reads,
                x.o4_2_reads,
                x.o4_3_reads,
                x.o4_4_reads,
                x.o4_5_reads,
                x.o4_6_reads,
                x.o4_7_reads,
                x.o4_8_reads,
                x.o4_9_reads,
                x.o4_10_reads,
                x.o4_11_reads,
                x.o4_12_reads,
                x.o4_13_reads,
                x.o4_14_reads,
                x.o4_15_reads,
                x.o4_16_reads,
                'skyblue',
                k
            ))
            i+=4
        return A
    
    new_A5_list = pt_sort(submitted_ordered)
     
    
    func = lambda x: (x[0])
    sort = sorted(new_A5_list, key = func, reverse=True)
    
    return render(request, "ees_forms/pt_mth_input.html", {
        "now": now, 'todays_log': todays_log, "back": back, "today": today, 'submitted_ordered': submitted_ordered, 'sort' : sort, 'profile':profile,
    })

def method303_rolling_avg(request):
    submitted_ordered = formA5_readings_model.objects.all()

    daily_prof = daily_battery_profile_model.objects.all().order_by('date_save')
    todays_log = daily_prof[0]
    
    A = []
    def form_compile(daily_prof):
        formA1 = formA1_readings_model.objects.all()
        formA2 = formA2_model.objects.all()
        formA3 = formA3_model.objects.all()
        i=1
        for date_select in daily_prof:
            print(date_select)

            for logA1 in formA1:
                if str(date_select.date_save) == str(logA1.form.date):
                    A1 = logA1
                    print('passA1')
                    print(A1)

                    for logA2 in formA2:
                        if date_select.date_save == logA2.date:
                            A2 = logA2
                            print('passA2')

                            for logA3 in formA3:
                                if date_select.date_save == logA3.date:
                                    A3 = logA3
                                    print('passA3')

                                    A.append((i, date_select.date_save, A1.c1_sec, A1.c2_sec, A1.c3_sec, A1.c4_sec, A1.c5_sec, A2.inop_ovens, A2.doors_not_observed, A2.leaking_doors, A3.inop_ovens, A3.l_not_observed, A3.l_leaks, A3.om_not_observed, A3.om_leaks))
                                    print(i)
                                    i+= 1
        return A
    
    list_of_records = form_compile(daily_prof)
    print(list_of_records)
    

    return render(request, "ees_forms/method303_rolling_avg.html", {
        "now": now, 'todays_log': todays_log, "back": back, "today": today, 'list_of_records':list_of_records, 'profile':profile,
    })

def profile(request, access_page):
    profile = user_profile_model.objects.all()
    current_user = request.user
    
    for x in profile:
        print(x.user)
        if x.user == current_user:
            user_select = x
            print(user_select)
    
    pic = user_select.profile_picture
    cert = user_select.cert_date
    user_sel = user_select.user
    
    
    initial_data = {
        'cert_date': user_select.cert_date,
        'profile_picture': user_select.profile_picture,
        'phone': user_select.phone,
        'position': user_select.position,
    }
    
    pic_form = user_profile_form(initial= initial_data)
    
    if request.method == "POST":
        form = user_profile_form(request.POST, request.FILES, instance = user_select)
        
        if form.is_valid():
            print('chicken')
            A = form.save(commit = False)
            A.cert_date = cert
            
            form.save()
            
            return redirect('../profile/main')
        
        
        print(form.errors)
        
        
        
        
        
    
    return render (request, "ees_forms/profile.html", {
        "back": back, 'todays_log': todays_log, 'user_select': user_select, "today": today, 'pic': pic, 'pic_form': pic_form, 'access_page': access_page, 'profile':profile, 
    })
@lock
def admin_data_view(request):
    profile = user_profile_model.objects.all()
    
    return render (request, "ees_forms/admin_data.html", {
        "back": back, 'todays_log': todays_log, "today": today, 'profile':profile,
    })
#------------------------------------------------------------------------A1---------------<
@lock
def formA1(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
    
    formName = "A1"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    org = formA1_model.objects.all().order_by('-date')
    database_form = org[0]
    org2 = formA1_readings_model.objects.all().order_by('-form')
    database_form2 = org2[0]
    
    full_name = request.user.get_full_name()
    
    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        data = database_model
        for x in org2:
            if str(x.form.date) == str(selector):
                database_model2 = x
        readings = database_model2
  
    else:
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'date' : database_form.date,
                        'observer' : database_form.observer,
                        'crew' : database_form.crew,
                        'foreman' : database_form.foreman,
                        'start' : database_form.start,
                        'stop' : database_form.stop,
                        'c1_no' : database_form2.c1_no,
                        'c2_no' : database_form2.c2_no,
                        'c3_no' : database_form2.c3_no,
                        'c4_no' : database_form2.c4_no,
                        'c5_no' : database_form2.c5_no,
                        'c1_start' : database_form2.c1_start,
                        'c2_start' : database_form2.c2_start,
                        'c3_start' : database_form2.c3_start,
                        'c4_start' : database_form2.c4_start,
                        'c5_start' : database_form2.c5_start,
                        'c1_stop' : database_form2.c1_stop,
                        'c2_stop' : database_form2.c2_stop,
                        'c3_stop' : database_form2.c3_stop,
                        'c4_stop' : database_form2.c4_stop,
                        'c5_stop' : database_form2.c5_stop,
                        'c1_sec' : database_form2.c1_sec,
                        'c2_sec' : database_form2.c2_sec,
                        'c3_sec' : database_form2.c3_sec,
                        'c4_sec' : database_form2.c4_sec,
                        'c5_sec' : database_form2.c5_sec,
                        'c1_comments' : database_form2.c1_comments,
                        'c2_comments' : database_form2.c2_comments,
                        'c3_comments' : database_form2.c3_comments,
                        'c4_comments' : database_form2.c4_comments,
                        'c5_comments' : database_form2.c5_comments,
                        'larry_car' : database_form2.larry_car,
                        'comments' : database_form2.comments,
                        'total_seconds' : database_form2.total_seconds,
                    }
                    data = formA1_form(initial=initial_data)
                    readings = formA1_readings_form(initial=initial_data)

                    if request.method == "POST":
                        form = formA1_form(request.POST, instance=database_form)
                        reads = formA1_readings_form(request.POST, instance=database_form2)

                        A_valid = form.is_valid()
                        B_valid = reads.is_valid()

                        if A_valid and B_valid:
                            A = form.save()
                            B = reads.save(commit=False)
                            B.form = A
                            B.save()

                       #     if B.comments not in {'-', 'n/a', 'N/A'}:
                       #         issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'
                        #            
                       #         return redirect (issue_page)
                            sec = {B.c1_sec, B.c2_sec, B.c3_sec, B.c4_sec, B.c5_sec}
                            for x in sec:
                                if 10 <= x:
                                    issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

                                    return redirect (issue_page)
                                else:
                                    if B.total_seconds >= 55:
                                        issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'

                                        return redirect (issue_page)
                            done = Forms.objects.filter(form='A-1')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')

                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name,
                        'crew' : todays_log.crew,
                        'foreman' : todays_log.foreman,
                    }
                    data = formA1_form(initial=initial_data)
                    readings = formA1_readings_form()
                    if request.method == "POST":
                        form = formA1_form(request.POST)
                        reads = formA1_readings_form(request.POST)
                        A_valid = form.is_valid()
                        B_valid = reads.is_valid()

                        if A_valid and B_valid:
                            A = form.save()
                            B = reads.save(commit=False)
                            B.form = A
                            B.save()

                    #        if B.comments not in {'-', 'n/a', 'N/A'}:
                    #            issue_page = '../../issues_view/A-1/' + str(todays_log.date_save) + '/form'
                    #                
                    #            return redirect (issue_page)
                            sec = {B.c1_sec, B.c2_sec, B.c3_sec, B.c4_sec, B.c5_sec}
                            for x in sec:
                                if 10 <= x:
                                    issue_page = '../../issues_view/A-1/' + str(todays_log.date_save) + '/form'

                                    return redirect (issue_page)
                                else:
                                    if B.total_seconds >= 55:
                                        issue_page = '../../issues_view/A-1/' + str(todays_log.date_save) + '/form'

                                        return redirect (issue_page)
                            done = Forms.objects.filter(form='A-1')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)
    
    return render (request, "Daily/formA1.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'readings': readings, 'formName':formName, 'profile':profile, 'selector': selector, "client": client, 'unlock': unlock
    })
#------------------------------------------------------------------------A2---------------<
@lock
def formA2(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
        
    formName = "A2"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    org = formA2_model.objects.all().order_by('-date')
    database_form = org[0]
    
    full_name = request.user.get_full_name()
    
    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        data = database_model
  
    else:
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'date' : database_form.date,
                        'observer' : database_form.observer,
                        'crew' : database_form.crew,
                        'foreman' : database_form.foreman,
                        'inop_ovens' : database_form.inop_ovens,
                        'p_start' : database_form.p_start,
                        'p_stop' : database_form.p_stop,
                        'c_start' : database_form.c_start,
                        'c_stop' : database_form.c_stop,
                        'p_leak_oven1' : database_form.p_leak_oven1,
                        'p_leak_loc1' : database_form.p_leak_loc1,
                        'p_leak_zone1' : database_form.p_leak_zone1,
                        'c_leak_oven1' : database_form.c_leak_oven1,
                        'c_leak_loc1' : database_form.c_leak_loc1,
                        'c_leak_zone1' : database_form.c_leak_zone1,
                        'notes' : database_form.notes,
                        'p_temp_block_from' : database_form.p_temp_block_from,
                        'p_temp_block_to' : database_form.p_temp_block_to,
                        'c_temp_block_from' : database_form.c_temp_block_from,
                        'c_temp_block_to' : database_form.c_temp_block_to,
                        'p_traverse_time_min' : database_form.p_traverse_time_min,
                        'p_traverse_time_sec' : database_form.p_traverse_time_sec,
                        'c_traverse_time_min' : database_form.c_traverse_time_min,
                        'c_traverse_time_sec' : database_form.c_traverse_time_sec,
                        'total_traverse_time' : database_form.total_traverse_time,
                        'allowed_traverse_time' : database_form.allowed_traverse_time,
                        'valid_run' : database_form.valid_run,
                        'leaking_doors' : database_form.leaking_doors,
                        'doors_not_observed' : database_form.doors_not_observed,
                        'inop_doors_eq' : database_form.inop_doors_eq,
                        'percent_leaking' : database_form.percent_leaking,
                    }
                    data = formA2_form(initial=initial_data)
                    if request.method == "POST":
                        form = formA2_form(request.POST, instance=database_form)
                        if form.is_valid():
                            A = form.save()

                            if A.notes not in {'-', 'n/a', 'N/A'}:
                                issue_page = '../../issues_view/A-2/' + str(database_form.date) + '/form'

                                return redirect (issue_page)

                            if A.leaking_doors == 0:
                                done = Forms.objects.filter(form='A-2')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                            else:
                                issue_page = '../../issues_view/A-2/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name,
                        'crew' : todays_log.crew,
                        'foreman' : todays_log.foreman,
                        'inop_ovens' : todays_log.inop_ovens,
                        'notes' : 'N/A',
                    }
                    data = formA2_form(initial=initial_data)
                    if request.method == "POST":
                        form = formA2_form(request.POST)
                        if form.is_valid():
                            A = form.save()

                            if A.notes not in {'-', 'n/a', 'N/A'}:
                                issue_page = '../../issues_view/A-2/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)

                            if A.leaking_doors == 0:
                                done = Forms.objects.filter(form='A-2')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                            else:
                                issue_page = '../../issues_view/A-2/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)

    return render (request, "Daily/formA2.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'formName':formName, 'profile':profile, 'selector': selector, 'client':client,
    })
#------------------------------------------------------------------------A3---------------<
@lock
def formA3(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
        
    formName = "A3"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    org = formA3_model.objects.all().order_by('-date')
    database_form = org[0]
    
    full_name = request.user.get_full_name()
    
    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        data = database_model
  
    else:
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'date' : database_form.date,
                        'observer' : database_form.observer,
                        'crew' : database_form.crew,
                        'foreman' : database_form.foreman,
                        'inop_ovens' : database_form.inop_ovens,
                        'om_start' : database_form.om_start,
                        'om_stop' : database_form.om_stop,
                        'l_start' : database_form.l_start,
                        'l_stop' : database_form.l_stop,
                        'om_oven1' : database_form.om_oven1,
                        'om_loc1' : database_form.om_loc1,
                        'l_oven1' : database_form.l_oven1,
                        'l_loc1' : database_form.l_loc1,
                        'om_traverse_time_min' : database_form.om_traverse_time_min,
                        'om_traverse_time_sec' : database_form.om_traverse_time_sec,
                        'l_traverse_time_min' : database_form.l_traverse_time_min,
                        'l_traverse_time_sec' : database_form.l_traverse_time_sec,
                        'om_allowed_traverse_time' : database_form.om_allowed_traverse_time,
                        'l_allowed_traverse_time' : database_form.l_allowed_traverse_time,
                        'om_valid_run' : database_form.om_valid_run,
                        'l_valid_run' : database_form.l_valid_run,
                        'om_leaks' : database_form.om_leaks,
                        'l_leaks' : database_form.l_leaks,
                        'om_not_observed' : database_form.om_not_observed,
                        'l_not_observed' : database_form.l_not_observed,
                        'om_percent_leaking' : database_form.om_percent_leaking,
                        'l_percent_leaking' : database_form.l_percent_leaking,
                        'notes' : database_form.notes,
                    }
                    data = formA3_form(initial=initial_data)
                    if request.method == "POST":
                        form = formA3_form(request.POST, instance= database_form)
                        if form.is_valid():
                            A = form.save()

                            if A.notes not in {'-', 'n/a', 'N/A'}:
                                issue_page = '../../issues_view/A-3/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            if int(A.om_leaks) > 0:
                                issue_page = '../../issues_view/A-3/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            if int(A.l_leaks) > 0:
                                issue_page = '../../issues_view/A-3/' + str(database_form.date) + '/form'

                                return redirect (issue_page)

                            done = Forms.objects.filter(form='A-3')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')

                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name,
                        'crew' : todays_log.crew,
                        'foreman' : todays_log.foreman,
                        'inop_ovens' : todays_log.inop_ovens,
                        'notes' : 'N/A',
                    }
                    data = formA3_form(initial=initial_data)
                    if request.method == "POST":
                        form = formA3_form(request.POST)
                        if form.is_valid():
                            A = form.save()

                            if A.notes not in {'-', 'n/a', 'N/A'}:
                                issue_page = '../../issues_view/A-3/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)
                            if int(A.om_leaks) > 0:
                                issue_page = '../../issues_view/A-3/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)
                            if int(A.l_leaks) > 0:
                                issue_page = '../../issues_view/A-3/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)

                            done = Forms.objects.filter(form='A-3')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)

    return render (request, "Daily/formA3.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'formName':formName, 'profile':profile, 'selector': selector, 'client':client,
    })
#------------------------------------------------------------------------A4---------------<
@lock
def formA4(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
    
    formName = "A4"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    org = formA4_model.objects.all().order_by('-date')
    database_form = org[0]
    
    full_name = request.user.get_full_name()
    
    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        data = database_model
  
    else:
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                if todays_log.date_save == database_form.date:
                    initial_data = {
                    'date' : database_form.date,
                    'observer' : database_form.observer,
                    'crew' : database_form.crew,
                    'foreman' : database_form.foreman,
                    'main_start' : database_form.main_start,
                    'main_stop' : database_form.main_stop,
                    'main_1' : database_form.main_1,
                    'main_2' : database_form.main_2,
                    'main_3' : database_form.main_3,
                    'main_4' : database_form.main_4,
                    'suction_main' : database_form.suction_main,
                    'oven_leak_1' : database_form.oven_leak_1,
                    'time_leak_1' : database_form.time_leak_1,
                    'date_temp_seal_leak_1' : database_form.date_temp_seal_leak_1,
                    'time_temp_seal_leak_1' : database_form.time_temp_seal_leak_1,
                    'temp_seal_by_leak_1' : database_form.temp_seal_by_leak_1,
                    'date_init_repair_leak_1' : database_form.date_init_repair_leak_1,
                    'time_init_repair_leak_1' : database_form.time_init_repair_leak_1,
                    'date_comp_repair_leak_1' : database_form.date_comp_repair_leak_1,
                    'time_comp_repair_leak_1' : database_form.time_comp_repair_leak_1,
                    'comp_by_leak_1' : database_form.comp_by_leak_1,
                    'notes' : database_form.notes,
                    }
                    data = formA4_form(initial=initial_data)

                    if request.method == "POST":
                        form = formA4_form(request.POST, instance=database_form)
                        if form.is_valid():
                            A = form.save()

                            if A.notes not in {'No VE', 'NO VE', 'no ve', 'no VE'}:
                                issue_page = '../../issues_view/A-4/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            if A.oven_leak_1:
                                issue_page = '../../issues_view/A-4/' + str(database_form.date) + '/form'

                                return redirect (issue_page)

                            done = Forms.objects.filter(form='A-4')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                        else:
                            print(form.errors)

                else:
                    initial_data = {
                    'date' : todays_log.date_save,
                    'observer' : full_name,
                    'crew' : todays_log.crew,
                    'foreman' : todays_log.foreman,
                    }
                    data = formA4_form(initial=initial_data)

                    if request.method == "POST":
                        form = formA4_form(request.POST)
                        if form.is_valid():
                            A = form.save()

                            if A.notes not in {'No VE', 'NO VE', 'no ve', 'no VE'}:
                                issue_page = '../../issues_view/A-4/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)
                            if A.oven_leak_1:
                                issue_page = '../../issues_view/A-4/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)

                            done = Forms.objects.filter(form='A-4')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)
    
    return render (request, "Daily/formA4.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'formName':formName, 'profile':profile, 'selector':selector, 'client':client,
    })
#------------------------------------------------------------------------A5---------------<
@lock
def formA5(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
         
    formName = "A5"
    profile = user_profile_model.objects.all()
    this_from = 'A-5'
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    org = formA5_model.objects.all().order_by('-date')
    database_form = org[0]
    org2 = formA5_readings_model.objects.all().order_by('-form')
    database_form2 = org2[0]
    
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    
    
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'

    city = 'Dearborn'

    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
    
    weather = {
        'city' : city,
        'temperature' : round(city_weather['main']['temp'],0),
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon'],
        'wind_speed' : round(city_weather['wind']['speed'],0),
        'wind_direction' : city_weather['wind']['deg'],
        'humidity' : city_weather['main']['humidity'],
    }
    
    degree = weather['wind_direction']
    
    
    def toTextualDescription(degree):
        if degree > 337.5:
            return 'N'
        if degree > 292.5:
            return 'NW'
        if degree > 247.5:
            return 'W'
        if degree > 202.5:
            return 'SW'
        if degree > 157.5:
            return 'S'
        if degree > 122.5:
            return 'SE'
        if degree > 67.5:
            return 'E'
        if degree > 22.5:
            return 'NE'
        return 'N'
    
    wind_direction = toTextualDescription(degree)
    
    
    
    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        data = database_model
        for x in org2:
            if str(x.form.date) == str(selector):
                database_model2 = x
        readings_form = database_model2
        profile_form = ''
    else:
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                if str(todays_log.date_save) == str(database_form.date):
                    initial_data = {
                        'date' : database_form.date,
                        'estab' : database_form.estab,
                        'county' : database_form.county,
                        'estab_no' : database_form.estab_no,
                        'equip_loc' : database_form.equip_loc,
                        'district' : database_form.district,
                        'city' : database_form.city,
                        'observer' : database_form.observer,
                        'cert_date' : database_form.cert_date,
                        'process_equip1' : database_form.process_equip1,
                        'process_equip2' : database_form.process_equip2,
                        'op_mode1' : database_form.op_mode1,
                        'op_mode2' : database_form.op_mode2,
                        'background_color_start' : database_form.background_color_start,
                        'background_color_stop' : database_form.background_color_stop,
                        'sky_conditions' : database_form.sky_conditions,
                        'wind_speed_start' : database_form.wind_speed_start,
                        'wind_speed_stop' : database_form.wind_speed_stop,
                        'wind_direction' : database_form.wind_direction,
                        'emission_point_start' : database_form.emission_point_start,
                        'emission_point_stop' : database_form.emission_point_stop,
                        'ambient_temp_start' : database_form.ambient_temp_start,
                        'ambient_temp_stop' : database_form.ambient_temp_stop,
                        'humidity' : database_form.humidity,
                        'height_above_ground' : database_form.height_above_ground,
                        'height_rel_observer' : database_form.height_rel_observer,
                        'distance_from' : database_form.distance_from,
                        'direction_from' : database_form.direction_from,
                        'describe_emissions_start' : database_form.describe_emissions_start,
                        'describe_emissions_stop' : database_form.describe_emissions_stop,
                        'emission_color_start' : database_form.emission_color_start,
                        'emission_color_stop' : database_form.emission_color_stop,
                        'plume_type' : database_form.plume_type,
                        'water_drolet_present' : database_form.water_drolet_present,
                        'water_droplet_plume' : database_form.water_droplet_plume,
                        'plume_opacity_determined_start' : database_form.plume_opacity_determined_start,
                        'plume_opacity_determined_stop' : database_form.plume_opacity_determined_stop,
                        'describe_background_start' : database_form.describe_background_start,
                        'describe_background_stop' : database_form.describe_background_stop,
                        'o1' : database_form2.o1,
                        'o1_start' : database_form2.o1_start,
                        'o1_stop' : database_form2.o1_stop,
                        'o1_highest_opacity' : database_form2.o1_highest_opacity,
                        'o1_instant_over_20' : database_form2.o1_instant_over_20,
                        'o1_average_6' : database_form2.o1_average_6,
                        'o1_average_6_over_35' : database_form2.o1_average_6_over_35,
                        'o2' : database_form2.o2,
                        'o2_start' : database_form2.o2_start,
                        'o2_stop' : database_form2.o2_stop,
                        'o2_highest_opacity' : database_form2.o2_highest_opacity,
                        'o2_instant_over_20' : database_form2.o2_instant_over_20,
                        'o2_average_6' : database_form2.o2_average_6,
                        'o2_average_6_over_35' : database_form2.o2_average_6_over_35,
                        'o3' : database_form2.o3,
                        'o3_start' : database_form2.o3_start,
                        'o3_stop' : database_form2.o3_stop,
                        'o3_highest_opacity' : database_form2.o3_highest_opacity,
                        'o3_instant_over_20' : database_form2.o3_instant_over_20,
                        'o3_average_6' : database_form2.o3_average_6,
                        'o3_average_6_over_35' : database_form2.o3_average_6_over_35,
                        'o4' : database_form2.o4,
                        'o4_start' : database_form2.o4_start,
                        'o4_stop' : database_form2.o4_stop,
                        'o4_highest_opacity' : database_form2.o4_highest_opacity,
                        'o4_instant_over_20' : database_form2.o4_instant_over_20,
                        'o4_average_6' : database_form2.o4_average_6,
                        'o4_average_6_over_35' : database_form2.o4_average_6_over_35,
                        'o1_1_reads' : database_form2.o1_1_reads,
                        'o1_2_reads' : database_form2.o1_2_reads,
                        'o1_3_reads' : database_form2.o1_3_reads,
                        'o1_4_reads' : database_form2.o1_4_reads,
                        'o1_5_reads' : database_form2.o1_5_reads,
                        'o1_6_reads' : database_form2.o1_6_reads,
                        'o1_7_reads' : database_form2.o1_7_reads,
                        'o1_8_reads' : database_form2.o1_8_reads,
                        'o1_9_reads' : database_form2.o1_9_reads,
                        'o1_10_reads' : database_form2.o1_10_reads,
                        'o1_11_reads' : database_form2.o1_11_reads,
                        'o1_12_reads' : database_form2.o1_12_reads,
                        'o1_13_reads' : database_form2.o1_13_reads,
                        'o1_14_reads' : database_form2.o1_14_reads,
                        'o1_15_reads' : database_form2.o1_15_reads,
                        'o1_16_reads' : database_form2.o1_16_reads,
                        'o2_1_reads' : database_form2.o2_1_reads,
                        'o2_2_reads' : database_form2.o2_2_reads,
                        'o2_3_reads' : database_form2.o2_3_reads,
                        'o2_4_reads' : database_form2.o2_4_reads,
                        'o2_5_reads' : database_form2.o2_5_reads,
                        'o2_6_reads' : database_form2.o2_6_reads,
                        'o2_7_reads' : database_form2.o2_7_reads,
                        'o2_8_reads' : database_form2.o2_8_reads,
                        'o2_9_reads' : database_form2.o2_9_reads,
                        'o2_10_reads' : database_form2.o2_10_reads,
                        'o2_11_reads' : database_form2.o2_11_reads,
                        'o2_12_reads' : database_form2.o2_12_reads,
                        'o2_13_reads' : database_form2.o2_13_reads,
                        'o2_14_reads' : database_form2.o2_14_reads,
                        'o2_15_reads' : database_form2.o2_15_reads,
                        'o2_16_reads' : database_form2.o2_16_reads,
                        'o3_1_reads' : database_form2.o3_1_reads,
                        'o3_2_reads' : database_form2.o3_2_reads,
                        'o3_3_reads' : database_form2.o3_3_reads,
                        'o3_4_reads' : database_form2.o3_4_reads,
                        'o3_5_reads' : database_form2.o3_5_reads,
                        'o3_6_reads' : database_form2.o3_6_reads,
                        'o3_7_reads' : database_form2.o3_7_reads,
                        'o3_8_reads' : database_form2.o3_8_reads,
                        'o3_9_reads' : database_form2.o3_9_reads,
                        'o3_10_reads' : database_form2.o3_10_reads,
                        'o3_11_reads' : database_form2.o3_11_reads,
                        'o3_12_reads' : database_form2.o3_12_reads,
                        'o3_13_reads' : database_form2.o3_13_reads,
                        'o3_14_reads' : database_form2.o3_14_reads,
                        'o3_15_reads' : database_form2.o3_15_reads,
                        'o3_16_reads' : database_form2.o3_16_reads,
                        'o4_1_reads' : database_form2.o4_1_reads,
                        'o4_2_reads' : database_form2.o4_2_reads,
                        'o4_3_reads' : database_form2.o4_3_reads,
                        'o4_4_reads' : database_form2.o4_4_reads,
                        'o4_5_reads' : database_form2.o4_5_reads,
                        'o4_6_reads' : database_form2.o4_6_reads,
                        'o4_7_reads' : database_form2.o4_7_reads,
                        'o4_8_reads' : database_form2.o4_8_reads,
                        'o4_9_reads' : database_form2.o4_9_reads,
                        'o4_10_reads' : database_form2.o4_10_reads,
                        'o4_11_reads' : database_form2.o4_11_reads,
                        'o4_12_reads' : database_form2.o4_12_reads,
                        'o4_13_reads' : database_form2.o4_13_reads,
                        'o4_14_reads' : database_form2.o4_14_reads,
                        'o4_15_reads' : database_form2.o4_15_reads,
                        'o4_16_reads' : database_form2.o4_16_reads,
                        'notes' : database_form.notes,
                    }
                    data = formA5_form(initial=initial_data)
                    readings_form = formA5_readings_form(initial=initial_data)
                    profile_form = user_profile_form()

                    if request.method == "POST":
                        form = formA5_form(request.POST, instance=database_form)
                        readings = formA5_readings_form(request.POST, instance=database_form2)
                        A_valid = form.is_valid()
                        B_valid = readings.is_valid()

                        print(form.errors)
                        print(readings.errors)
                        if A_valid and B_valid:
                            A = form.save()
                            B = readings.save(commit=False)

                            B.form = A
                            B.save()

                            if B.o1_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o1_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o1_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o1_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            
                            
                            
                            if B.o2_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o2_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o2_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o2_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            
                            
                            
                            
                            if B.o3_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o3_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o3_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o3_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            
                            
                            
                            
                            if B.o4_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o4_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o4_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o4_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)


                            done = Forms.objects.filter(form='A-5')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
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
                        'describe_background_stop' : "Same",
                        'sky_conditions' : weather['description'],
                        'wind_speed_start' : weather['wind_speed'],
                        'wind_direction' : wind_direction,
                        'ambient_temp_start' : weather['temperature'],
                        'humidity' : weather['humidity'],
                    }
                    data = formA5_form(initial=initial_data)
                    profile_form = user_profile_form()
                    readings_form = formA5_readings_form()

                    if request.method == "POST":
                        form = formA5_form(request.POST)
                        readings = formA5_readings_form(request.POST)
                        A_valid = form.is_valid()
                        B_valid = readings.is_valid()

                        print(form.errors)
                        print(readings.errors)
                        if A_valid and B_valid:
                            A = form.save()
                            B = readings.save(commit=False)

                            B.form = A
                            B.save()

                            if B.o1_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o1_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o1_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o1_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            
                            
                            
                            if B.o2_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o2_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o2_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o2_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            
                            
                            
                            
                            if B.o3_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o3_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o3_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o3_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            
                            
                            
                            
                            if B.o4_highest_opacity >= 10:
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o4_average_6 >= 35 :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                return redirect (issue_page)
                            
                            if B.o4_instant_over_20 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)
                            
                            if B.o4_average_6_over_35 == 'Yes' :
                                issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'
                                
                                return redirect (issue_page)

                            done = Forms.objects.filter(form='A-5')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                    else:
                        form = formA5_form(initial=initial_data)
                        readings_form = formA5_readings_form()
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)
                    
    return render (request, "Daily/formA5.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'profile_form': profile_form, 'readings_form': readings_form, 'formName': formName, 'profile':profile, 'selector': selector, 'client':client, 'unlock':unlock,
    })
#------------------------------------------------------------------------FORM B---------------<
@lock
def formB(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    one_week = datetime.timedelta(days=4)
    end_week = last_monday + one_week
    
    week_start_dates = formB_model.objects.all().order_by('-week_start')
    week_almost = week_start_dates[0]
    #last submitted monday
    week = week_almost.week_start
    week_fri = week_almost.week_end
    
    sunday = today - datetime.timedelta(days=1)
    
    if selector != 'form':
        for x in week_start_dates:
            if str(x.week_start) == str(selector):
                database_model = x
        data = database_model
        
    else:
        if today.weekday() not in {5, 6}:
            if week == last_monday:
                database_form = week_almost
                initial_data = {
                    'week_start' : database_form.week_start,
                    'week_end' : database_form.week_end,
                    'observer_0' : database_form.observer_0,
                    'time_0' : database_form.time_0,
                    'weather_0' : database_form.weather_0,
                    'wind_speed_0' : database_form.wind_speed_0,
                    'fugitive_dust_observed_0' : database_form.fugitive_dust_observed_0,
                    'supressant_applied_0' : database_form.supressant_applied_0,
                    'supressant_active_0' : database_form.supressant_active_0,
                    'working_face_exceed_0' : database_form.working_face_exceed_0,
                    'spills_0' : database_form.spills_0,
                    'pushed_back_0' : database_form.pushed_back_0,
                    'coal_vessel_0' : database_form.coal_vessel_0,
                    'water_sprays_0' : database_form.water_sprays_0,
                    'loader_lowered_0' : database_form.loader_lowered_0,
                    'working_water_sprays_0' : database_form.working_water_sprays_0,
                    'barrier_thickness_0' : database_form.barrier_thickness_0,
                    'surface_quality_0' : database_form.surface_quality_0,
                    'surpressant_crust_0' : database_form.surpressant_crust_0,
                    'additional_surpressant_0' : database_form.additional_surpressant_0,
                    'comments_0' : database_form.comments_0,
                    'wharf_0' : database_form.wharf_0,
                    'breeze_0' : database_form.breeze_0,

                    'observer_1' : database_form.observer_1,
                    'time_1' : database_form.time_1,
                    'weather_1' : database_form.weather_1,
                    'wind_speed_1' : database_form.wind_speed_1,
                    'fugitive_dust_observed_1' : database_form.fugitive_dust_observed_1,
                    'supressant_applied_1' : database_form.supressant_applied_1,
                    'supressant_active_1' : database_form.supressant_active_1,
                    'working_face_exceed_1' : database_form.working_face_exceed_1,
                    'spills_1' : database_form.spills_1,
                    'pushed_back_1' : database_form.pushed_back_1,
                    'coal_vessel_1' : database_form.coal_vessel_1,
                    'water_sprays_1' : database_form.water_sprays_1,
                    'loader_lowered_1' : database_form.loader_lowered_1,
                    'working_water_sprays_1' : database_form.working_water_sprays_1,
                    'barrier_thickness_1' : database_form.barrier_thickness_1,
                    'surface_quality_1' : database_form.surface_quality_1,
                    'surpressant_crust_1' : database_form.surpressant_crust_1,
                    'additional_surpressant_1' : database_form.additional_surpressant_1,
                    'comments_1' : database_form.comments_1,
                    'wharf_1' : database_form.wharf_1,
                    'breeze_1' : database_form.breeze_1,

                    'observer_2' : database_form.observer_2,
                    'time_2' : database_form.time_2,
                    'weather_2' : database_form.weather_2,
                    'wind_speed_2' : database_form.wind_speed_2,
                    'fugitive_dust_observed_2' : database_form.fugitive_dust_observed_2,
                    'supressant_applied_2' : database_form.supressant_applied_2,
                    'supressant_active_2' : database_form.supressant_active_2,
                    'working_face_exceed_2' : database_form.working_face_exceed_2,
                    'spills_2' : database_form.spills_2,
                    'pushed_back_2' : database_form.pushed_back_2,
                    'coal_vessel_2' : database_form.coal_vessel_2,
                    'water_sprays_2' : database_form.water_sprays_2,
                    'loader_lowered_2' : database_form.loader_lowered_2,
                    'working_water_sprays_2' : database_form.working_water_sprays_2,
                    'barrier_thickness_2' : database_form.barrier_thickness_2,
                    'surface_quality_2' : database_form.surface_quality_2,
                    'surpressant_crust_2' : database_form.surpressant_crust_2,
                    'additional_surpressant_2' : database_form.additional_surpressant_2,
                    'comments_2' : database_form.comments_2,
                    'wharf_2' : database_form.wharf_2,
                    'breeze_2' : database_form.breeze_2,

                    'observer_3' : database_form.observer_3,
                    'time_3' : database_form.time_3,
                    'weather_3' : database_form.weather_3,
                    'wind_speed_3' : database_form.wind_speed_3,
                    'fugitive_dust_observed_3' : database_form.fugitive_dust_observed_3,
                    'supressant_applied_3' : database_form.supressant_applied_3,
                    'supressant_active_3' : database_form.supressant_active_3,
                    'working_face_exceed_3' : database_form.working_face_exceed_3,
                    'spills_3' : database_form.spills_3,
                    'pushed_back_3' : database_form.pushed_back_3,
                    'coal_vessel_3' : database_form.coal_vessel_3,
                    'water_sprays_3' : database_form.water_sprays_3,
                    'loader_lowered_3' : database_form.loader_lowered_3,
                    'working_water_sprays_3' : database_form.working_water_sprays_3,
                    'barrier_thickness_3' : database_form.barrier_thickness_3,
                    'surface_quality_3' : database_form.surface_quality_3,
                    'surpressant_crust_3' : database_form.surpressant_crust_3,
                    'additional_surpressant_3' : database_form.additional_surpressant_3,
                    'comments_3' : database_form.comments_3,
                    'wharf_3' : database_form.wharf_3,
                    'breeze_3' : database_form.breeze_3,

                    'observer_4' : database_form.observer_4,
                    'time_4' : database_form.time_4,
                    'weather_4' : database_form.weather_4,
                    'wind_speed_4' : database_form.wind_speed_4,
                    'fugitive_dust_observed_4' : database_form.fugitive_dust_observed_4,
                    'supressant_applied_4' : database_form.supressant_applied_4,
                    'supressant_active_4' : database_form.supressant_active_4,
                    'working_face_exceed_4' : database_form.working_face_exceed_4,
                    'spills_4' : database_form.spills_4,
                    'pushed_back_4' : database_form.pushed_back_4,
                    'coal_vessel_4' : database_form.coal_vessel_4,
                    'water_sprays_4' : database_form.water_sprays_4,
                    'loader_lowered_4' : database_form.loader_lowered_4,
                    'working_water_sprays_4' : database_form.working_water_sprays_4,
                    'barrier_thickness_4' : database_form.barrier_thickness_4,
                    'surface_quality_4' : database_form.surface_quality_4,
                    'surpressant_crust_4' : database_form.surpressant_crust_4,
                    'additional_surpressant_4' : database_form.additional_surpressant_4,
                    'comments_4' : database_form.comments_4,
                    'wharf_4' : database_form.wharf_4,
                    'breeze_4' : database_form.breeze_4,

                }
                data = formB_form(initial=initial_data)
                done = Forms.objects.filter(form='B')[0]
                if request.method == "POST":
                    form = formB_form(request.POST, instance=week_almost)
                    A_valid = form.is_valid()
                    if A_valid:
                        form.save()

                        filled_out = True
                        for items in week_almost.whatever().values():
                            if items == None:
                                filled_out = True
                                break

                        if filled_out:
                            done = Forms.objects.filter(form='B')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()
                        else:
                            done.submitted = False
                            done.save()

                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'week_start' : last_monday,
                    'week_end' : end_week,
                }
                data = formB_form(initial= initial_data)
                if request.method == "POST":
                    form = formB_form(request.POST)
                    A_valid = form.is_valid()
                    if A_valid:
                        form.save()

                        done = Forms.objects.filter(form='B')[0]
                        filled_out = True
                        for items in week_almost.whatever().values():
                            if items == None:
                                filled_out = True
                                break
                        if filled_out: 
                            done = Forms.objects.filter(form='B')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()
                        else:
                            done.submitted = False
                            done.save()

                    return redirect('IncompleteForms')
        else:
            database_form = week_almost
            initial_data = {
                'week_start' : database_form.week_start,
                'week_end' : database_form.week_end,
                'observer_0' : database_form.observer_0,
                'time_0' : database_form.time_0,
                'weather_0' : database_form.weather_0,
                'wind_speed_0' : database_form.wind_speed_0,
                'fugitive_dust_observed_0' : database_form.fugitive_dust_observed_0,
                'supressant_applied_0' : database_form.supressant_applied_0,
                'supressant_active_0' : database_form.supressant_active_0,
                'working_face_exceed_0' : database_form.working_face_exceed_0,
                'spills_0' : database_form.spills_0,
                'pushed_back_0' : database_form.pushed_back_0,
                'coal_vessel_0' : database_form.coal_vessel_0,
                'water_sprays_0' : database_form.water_sprays_0,
                'loader_lowered_0' : database_form.loader_lowered_0,
                'working_water_sprays_0' : database_form.working_water_sprays_0,
                'barrier_thickness_0' : database_form.barrier_thickness_0,
                'surface_quality_0' : database_form.surface_quality_0,
                'surpressant_crust_0' : database_form.surpressant_crust_0,
                'additional_surpressant_0' : database_form.additional_surpressant_0,
                'comments_0' : database_form.comments_0,
                'wharf_0' : database_form.wharf_0,
                'breeze_0' : database_form.breeze_0,

                'observer_1' : database_form.observer_1,
                'time_1' : database_form.time_1,
                'weather_1' : database_form.weather_1,
                'wind_speed_1' : database_form.wind_speed_1,
                'fugitive_dust_observed_1' : database_form.fugitive_dust_observed_1,
                'supressant_applied_1' : database_form.supressant_applied_1,
                'supressant_active_1' : database_form.supressant_active_1,
                'working_face_exceed_1' : database_form.working_face_exceed_1,
                'spills_1' : database_form.spills_1,
                'pushed_back_1' : database_form.pushed_back_1,
                'coal_vessel_1' : database_form.coal_vessel_1,
                'water_sprays_1' : database_form.water_sprays_1,
                'loader_lowered_1' : database_form.loader_lowered_1,
                'working_water_sprays_1' : database_form.working_water_sprays_1,
                'barrier_thickness_1' : database_form.barrier_thickness_1,
                'surface_quality_1' : database_form.surface_quality_1,
                'surpressant_crust_1' : database_form.surpressant_crust_1,
                'additional_surpressant_1' : database_form.additional_surpressant_1,
                'comments_1' : database_form.comments_1,
                'wharf_1' : database_form.wharf_1,
                'breeze_1' : database_form.breeze_1,

                'observer_2' : database_form.observer_2,
                'time_2' : database_form.time_2,
                'weather_2' : database_form.weather_2,
                'wind_speed_2' : database_form.wind_speed_2,
                'fugitive_dust_observed_2' : database_form.fugitive_dust_observed_2,
                'supressant_applied_2' : database_form.supressant_applied_2,
                'supressant_active_2' : database_form.supressant_active_2,
                'working_face_exceed_2' : database_form.working_face_exceed_2,
                'spills_2' : database_form.spills_2,
                'pushed_back_2' : database_form.pushed_back_2,
                'coal_vessel_2' : database_form.coal_vessel_2,
                'water_sprays_2' : database_form.water_sprays_2,
                'loader_lowered_2' : database_form.loader_lowered_2,
                'working_water_sprays_2' : database_form.working_water_sprays_2,
                'barrier_thickness_2' : database_form.barrier_thickness_2,
                'surface_quality_2' : database_form.surface_quality_2,
                'surpressant_crust_2' : database_form.surpressant_crust_2,
                'additional_surpressant_2' : database_form.additional_surpressant_2,
                'comments_2' : database_form.comments_2,
                'wharf_2' : database_form.wharf_2,
                'breeze_2' : database_form.breeze_2,

                'observer_3' : database_form.observer_3,
                'time_3' : database_form.time_3,
                'weather_3' : database_form.weather_3,
                'wind_speed_3' : database_form.wind_speed_3,
                'fugitive_dust_observed_3' : database_form.fugitive_dust_observed_3,
                'supressant_applied_3' : database_form.supressant_applied_3,
                'supressant_active_3' : database_form.supressant_active_3,
                'working_face_exceed_3' : database_form.working_face_exceed_3,
                'spills_3' : database_form.spills_3,
                'pushed_back_3' : database_form.pushed_back_3,
                'coal_vessel_3' : database_form.coal_vessel_3,
                'water_sprays_3' : database_form.water_sprays_3,
                'loader_lowered_3' : database_form.loader_lowered_3,
                'working_water_sprays_3' : database_form.working_water_sprays_3,
                'barrier_thickness_3' : database_form.barrier_thickness_3,
                'surface_quality_3' : database_form.surface_quality_3,
                'surpressant_crust_3' : database_form.surpressant_crust_3,
                'additional_surpressant_3' : database_form.additional_surpressant_3,
                'comments_3' : database_form.comments_3,
                'wharf_3' : database_form.wharf_3,
                'breeze_3' : database_form.breeze_3,

                'observer_4' : database_form.observer_4,
                'time_4' : database_form.time_4,
                'weather_4' : database_form.weather_4,
                'wind_speed_4' : database_form.wind_speed_4,
                'fugitive_dust_observed_4' : database_form.fugitive_dust_observed_4,
                'supressant_applied_4' : database_form.supressant_applied_4,
                'supressant_active_4' : database_form.supressant_active_4,
                'working_face_exceed_4' : database_form.working_face_exceed_4,
                'spills_4' : database_form.spills_4,
                'pushed_back_4' : database_form.pushed_back_4,
                'coal_vessel_4' : database_form.coal_vessel_4,
                'water_sprays_4' : database_form.water_sprays_4,
                'loader_lowered_4' : database_form.loader_lowered_4,
                'working_water_sprays_4' : database_form.working_water_sprays_4,
                'barrier_thickness_4' : database_form.barrier_thickness_4,
                'surface_quality_4' : database_form.surface_quality_4,
                'surpressant_crust_4' : database_form.surpressant_crust_4,
                'additional_surpressant_4' : database_form.additional_surpressant_4,
                'comments_4' : database_form.comments_4,
                'wharf_4' : database_form.wharf_4,
                'breeze_4' : database_form.breeze_4,

            }
            data = formB_form(initial=initial_data)
            done = Forms.objects.filter(form='B')[0]
            if request.method == "POST":
                form = formB_form(request.POST, instance=week_almost)
                A_valid = form.is_valid()
                if A_valid:
                    form.save()

                    filled_out = True
                    for items in week_almost.whatever().values():
                        if items == None:
                            filled_out = False
                            break

                    if filled_out:
                        done = Forms.objects.filter(form='B')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()
                    else:
                        done.submitted = False
                        done.save()

                return redirect('IncompleteForms')
        
    return render (request, "Daily/formB.html", {
        "back": back, 'todays_log': todays_log, 'week': week, 'week_almost': week_almost, 'end_week': end_week, 'data': data, 'profile':profile, 'selector':selector
    })

#------------------------------------------------------------------------FORM C---------------<
@lock
def formC(request, selector):
    formName = "C"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    full_name = request.user.get_full_name()
    profile_user = user_profile_model.objects.all()
    
    org = formC_model.objects.all()
    org2 = formC_readings_model.objects.all()
    
    
    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        form = database_model
        for x in org2:
            if str(x.form.date) == str(selector):
                database_model2 = x
        read = database_model2
    else:
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                for x in profile_user:
                    if str(x.user) == str(request.user):
                        certification = x.cert_date

                count1 = formC_model.objects.count()
                count2 = formC_readings_model.objects.count()

                if count1 and count2 != 0:
                    org = formC_model.objects.all().order_by('-date')
                    database_form = org[0]
                    org2 = formC_readings_model.objects.all().order_by('-form')
                    database_form2 = org2[0]

                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'date' : database_form.date,
                            'truck_sel' : database_form.truck_sel,
                            'area_sel' : database_form.area_sel,
                            'truck_start_time' : database_form.truck_start_time,
                            'truck_stop_time' : database_form.truck_stop_time,
                            'area_start_time' : database_form.area_start_time,
                            'area_stop_time' : database_form.area_stop_time,
                            'observer' : database_form.observer,
                            'cert_date' : database_form.cert_date,
                            'comments' : database_form.comments,
                            'average_t' : database_form.average_t,
                            'average_p' : database_form.average_p,

                            'TRead1' : database_form2.TRead1,
                            'TRead2' : database_form2.TRead2,
                            'TRead3' : database_form2.TRead3,
                            'TRead4' : database_form2.TRead4,
                            'TRead5' : database_form2.TRead5,
                            'TRead6' : database_form2.TRead6,
                            'TRead7' : database_form2.TRead7,
                            'TRead8' : database_form2.TRead8,
                            'TRead9' : database_form2.TRead9,
                            'TRead10' : database_form2.TRead10,
                            'TRead11' : database_form2.TRead11,
                            'TRead12' : database_form2.TRead12,
                            'ARead1' : database_form2.ARead1,
                            'ARead2' : database_form2.ARead2,
                            'ARead3' : database_form2.ARead3,
                            'ARead4' : database_form2.ARead4,
                            'ARead5' : database_form2.ARead5,
                            'ARead6' : database_form2.ARead6,
                            'ARead7' : database_form2.ARead7,
                            'ARead8' : database_form2.ARead8,
                            'ARead9' : database_form2.ARead9,
                            'ARead10' : database_form2.ARead10,
                            'ARead11' : database_form2.ARead11,
                            'ARead12' : database_form2.ARead12,
                        }
                        form = SubFormC1(initial=initial_data)
                        read = FormCReadForm(initial=initial_data)

                        if request.method == "POST":
                            CData = SubFormC1(request.POST,instance = database_form )
                            CReadings = FormCReadForm(request.POST, instance = database_form2 )
                            A_valid = CReadings.is_valid()
                            B_valid = CData.is_valid()

                            if A_valid and B_valid:
                                A = CData.save()
                                B = CReadings.save(commit=False)
                                B.form = A
                                B.save()

                                if B.form.average_t > 5:
                                    issue_page = '../../issues_view/C/' + str(database_form.date) + '/form'

                                    return redirect (issue_page)
                                if B.form.average_p > 5:
                                    issue_page = '../../issues_view/C/' + str(database_form.date) + '/form'

                                    return redirect (issue_page)

                                if A.comments not in {'-', 'n/a', 'N/A'}:
                                    issue_page = '../../issues_view/C/' + str(database_form.date) + '/form'

                                    return redirect (issue_page)

                                done = Forms.objects.filter(form='C')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        for x in profile_user:
                            if x.user == User:
                                certification = x.cert_date

                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name,
                            'cert_date' : certification,
                        }

                        form = SubFormC1(initial=initial_data)
                        read = FormCReadForm()
                        if request.method == "POST":
                            CReadings = FormCReadForm(request.POST)
                            CData = SubFormC1(request.POST)
                            A_valid = CReadings.is_valid()
                            B_valid = CData.is_valid()

                            if A_valid and B_valid:
                                A = CData.save()
                                B = CReadings.save(commit=False)
                                B.form = A
                                B.save()

                                if B.form.average_t > 5:
                                    issue_page = '../../issues_view/C/' + str(todays_log.date_save) + '/form'

                                    return redirect (issue_page)
                                if B.form.average_p > 5:
                                    issue_page = '../../issues_view/C/' + str(todays_log.date_save) + '/form'

                                    return redirect (issue_page)

                                if A.comments not in {'-', 'n/a', 'N/A'}:
                                    issue_page = '../../issues_view/C/' + str(todays_log.date_save) + '/form'

                                    return redirect (issue_page)

                                done = Forms.objects.filter(form='C')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    for x in profile_user:
                            if x.user == User:
                                certification = x.cert_date

                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name,
                        'cert_date' : certification,
                    }

                    form = SubFormC1(initial=initial_data)
                    read = FormCReadForm()

                    if request.method == "POST":
                        CReadings = FormCReadForm(request.POST)
                        CData = SubFormC1(request.POST)
                        A_valid = CReadings.is_valid()
                        B_valid = CData.is_valid()

                        if A_valid and B_valid:
                            A = CData.save()
                            B = CReadings.save(commit=False)
                            B.form = A
                            B.save()

                            if B.form.average_t > 5:
                                issue_page = '../../issues_view/C/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)
                            if B.form.average_p > 5:
                                issue_page = '../../issues_view/C/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)

                            if B.comments not in {'-', 'n/a', 'N/A'}:
                                issue_page = '../../issues_view/C/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)

                            done = Forms.objects.filter(form='C')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)
        
    return render (request, "Daily/formC.html", {
        'form': form, 'read': read, "back": back,'profile':profile, 'selector': selector,
    })

#------------------------------------------------------------------------FORM D---------------<
@lock
def formD(request, selector):
    formName = "D"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    last_friday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_friday + one_week
    
    
    week_start_dates = formD_model.objects.all().order_by('-week_start')
    
    if not DBEmpty(week_start_dates):
        week_almost = week_start_dates[0]
        #last submitted saturday
        week = week_almost.week_start
        week_fri = week_almost.week_end

        sunday = today - datetime.timedelta(days=1)
        
        if today.weekday() not in {5, 6}:
            
            if week == last_friday:
                data = week_almost
                initial_data = {
                    'week_start' : data.week_start,
                    'week_end' : data.week_end,
                    'truck_id1' : data.truck_id1, 
                    'date1' : data.date1,
                    'time1' : data.time1,
                    'contents1' : data.contents1,
                    'freeboard1' : data.freeboard1,
                    'wetted1' : data.wetted1,
                    'comments1' : data.comments1,
                    'truck_id2' : data.truck_id2,
                    'date2' : data.date2,
                    'time2' : data.time2,
                    'contents2' : data.contents2,
                    'freeboard2' : data.freeboard2,
                    'wetted2' : data.wetted2,
                    'comments2' : data.comments2,
                    'truck_id3' : data.truck_id3,
                    'date3' : data.date3,
                    'time3' : data.time3,
                    'contents3' : data.contents3,
                    'freeboard3' : data.freeboard3,
                    'wetted3' : data.wetted3,
                    'comments3' : data.comments3,
                    'truck_id4' : data.truck_id4,
                    'date4' : data.date4,
                    'time4' : data.time4,
                    'contents4' : data.contents4,
                    'freeboard4' : data.freeboard4,
                    'wetted4' : data.wetted4,
                    'comments4' : data.comments4,
                    'truck_id5' : data.truck_id5,
                    'date5' : data.date5,
                    'time5' : data.time5,
                    'contents5' : data.contents5,
                    'freeboard5' : data.freeboard5,
                    'wetted5' : data.wetted5,
                    'comments5' : data.comments5,
                    'observer1' : data.observer1,
                    'observer2' : data.observer2,
                    'observer3' : data.observer3,
                    'observer4' : data.observer4,
                    'observer5' : data.observer5
                }
                empty_form = formD_form(initial=initial_data)
            
                if request.method == "POST":
                    form = formD_form(request.POST, instance=data)
                    A_valid = form.is_valid()
                    if A_valid:
                        form.save()

                        filled_out = True

                        for items in week_almost.whatever().values():
                            if items == None:
                                filled_out = True #-change this back to false
                                break

                        if filled_out:
                            done = Forms.objects.filter(form='D')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()
                        else:
                            done = Forms.objects.filter(form='D')[0]
                            done.submitted = False
                            done.save()

                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'week_start' : last_friday,
                    'week_end' : end_week
                }
                empty_form = formD_form(initial= initial_data)
                done = Forms.objects.filter(form='D')[0]
                if request.method == "POST":
                    form = formD_form(request.POST)
                    A_valid = form.is_valid()
                    if A_valid:
                        form.save()

                        filled_out = True

                        for items in week_almost.whatever().values():
                            if items == None:
                                filled_out = False
                                break

                        if filled_out:
                            done = Forms.objects.filter(form='D')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()
                        else:
                            done = Forms.objects.filter(form='D')[0]
                            done.submitted = False
                            done.save()



                    return redirect('IncompleteForms')
        
        else:
            if today.weekday() == 5 :
                if week == today:
                    print (week)
                    print (today)
                    data = week_almost
                    initial_data = {
                        'week_start' : data.week_start,
                        'week_end' : data.week_end,
                        'truck_id1' : data.truck_id1, 
                        'date1' : data.date1,
                        'time1' : data.time1,
                        'contents1' : data.contents1,
                        'freeboard1' : data.freeboard1,
                        'wetted1' : data.wetted1,
                        'comments1' : data.comments1,
                        'truck_id2' : data.truck_id2,
                        'date2' : data.date2,
                        'time2' : data.time2,
                        'contents2' : data.contents2,
                        'freeboard2' : data.freeboard2,
                        'wetted2' : data.wetted2,
                        'comments2' : data.comments2,
                        'truck_id3' : data.truck_id3,
                        'date3' : data.date3,
                        'time3' : data.time3,
                        'contents3' : data.contents3,
                        'freeboard3' : data.freeboard3,
                        'wetted3' : data.wetted3,
                        'comments3' : data.comments3,
                        'truck_id4' : data.truck_id4,
                        'date4' : data.date4,
                        'time4' : data.time4,
                        'contents4' : data.contents4,
                        'freeboard4' : data.freeboard4,
                        'wetted4' : data.wetted4,
                        'comments4' : data.comments4,
                        'truck_id5' : data.truck_id5,
                        'date5' : data.date5,
                        'time5' : data.time5,
                        'contents5' : data.contents5,
                        'freeboard5' : data.freeboard5,
                        'wetted5' : data.wetted5,
                        'comments5' : data.comments5,
                        'observer1' : data.observer1,
                        'observer2' : data.observer2,
                        'observer3' : data.observer3,
                        'observer4' : data.observer4,
                        'observer5' : data.observer5,

                    }
                    empty_form = formD_form(initial=initial_data)
                    done = Forms.objects.filter(form='D')[0]
                    if request.method == "POST":
                        form = formD_form(request.POST, instance=week_almost)
                        A_valid = form.is_valid()
                        if A_valid:
                            form.save()
                            print('hello')
                            print('')
                            filled_out = True
                            for items in week_almost.whatever().values():
                                if items == None:
                                    filled_out = False
                                    break

                            if filled_out:
                                done = Forms.objects.filter(form='D')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()
                            else:
                                done.submitted = False
                                done.save()

                        return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'week_start' : last_friday,
                        'week_end' : end_week
                    }
                    empty_form = formD_form(initial= initial_data)
                    done = Forms.objects.filter(form='D')[0]
                    if request.method == "POST":
                        form = formD_form(request.POST)
                        A_valid = form.is_valid()
                        if A_valid:
                            form.save()

                            filled_out = True
                            for items in week_almost.whatever().values():
                                if items == None:
                                    filled_out = False
                                    break
                            if filled_out: 
                                done = Forms.objects.filter(form='D')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()
                            else:
                                done.submitted = False
                                done.save()

                        return redirect('IncompleteForms')

            else:
                sunday = today - datetime.timedelta(days=1)
                if week == sunday:
                    data = week_almost
                    initial_data = {
                        'week_start' : data.week_start,
                        'week_end' : data.week_end,
                        'truck_id1' : data.truck_id1, 
                        'date1' : data.date1,
                        'time1' : data.time1,
                        'contents1' : data.contents1,
                        'freeboard1' : data.freeboard1,
                        'wetted1' : data.wetted1,
                        'comments1' : data.comments1,
                        'truck_id2' : data.truck_id2,
                        'date2' : data.date2,
                        'time2' : data.time2,
                        'contents2' : data.contents2,
                        'freeboard2' : data.freeboard2,
                        'wetted2' : data.wetted2,
                        'comments2' : data.comments2,
                        'truck_id3' : data.truck_id3,
                        'date3' : data.date3,
                        'time3' : data.time3,
                        'contents3' : data.contents3,
                        'freeboard3' : data.freeboard3,
                        'wetted3' : data.wetted3,
                        'comments3' : data.comments3,
                        'truck_id4' : data.truck_id4,
                        'date4' : data.date4,
                        'time4' : data.time4,
                        'contents4' : data.contents4,
                        'freeboard4' : data.freeboard4,
                        'wetted4' : data.wetted4,
                        'comments4' : data.comments4,
                        'truck_id5' : data.truck_id5,
                        'date5' : data.date5,
                        'time5' : data.time5,
                        'contents5' : data.contents5,
                        'freeboard5' : data.freeboard5,
                        'wetted5' : data.wetted5,
                        'comments5' : data.comments5,
                        'observer1' : data.observer1,
                        'observer2' : data.observer2,
                        'observer3' : data.observer3,
                        'observer4' : data.observer4,
                        'observer5' : data.observer5,

                    }
                    empty_form = formD_form(initial=initial_data)
                    done = Forms.objects.filter(form='D')[0]
                    if request.method == "POST":
                        form = formD_form(request.POST, instance=data)
                        A_valid = form.is_valid()
                        if A_valid:
                            form.save()
                            
                            filled_out = True
                            for items in week_almost.whatever().values():
                                if items == None:
                                    filled_out = True #-change this back to false
                                    break

                            if filled_out:
                                done = Forms.objects.filter(form='D')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()
                            else:
                                done.submitted = False
                                done.save()

                        return redirect('IncompleteForms')
                else:
                    
                    initial_data = {
                        'week_start' : sunday,
                        'week_end' : sunday + one_week,
                    }
                    empty_form = formD_form(initial= initial_data)
                    done = Forms.objects.filter(form='D')[0]
                    if request.method == "POST":
                        form = formD_form(request.POST)
                        A_valid = form.is_valid()
                        if A_valid:
                            form.save()
                            week_almost = week_start_dates[0]
                            filled_out = True
                            for items in week_almost.whatever().values():
                                if items == None:
                                    filled_out = False
                                    break
                            if filled_out: 
                                done = Forms.objects.filter(form='D')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()
                            else:
                                done.submitted = False
                                done.save()

                        return redirect('IncompleteForms')
        
    return render (request, "Weekly/formD.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'profile': profile, 'selector': selector,
    })
#----------------------------------------------------------------------FORM E---------------<
@lock
def formE(request, selector):
    profile = user_profile_model.objects.all()
    formName = "E"
    
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    
    
    full_name = request.user.get_full_name()
    
    if formE_model.objects.count() != 0:
        org = formE_model.objects.all().order_by('-date')
        database_form = org[0]
        if todays_log.date_save == database_form.date:
            initial_data = {
                'observer' : database_form.observer,
                'date' : database_form.date,
                'crew' : database_form.crew,
                'foreman' : database_form.foreman,
                'start_time' : database_form.start_time,
                'end_time' : database_form.end_time,
                'leaks' : database_form.leaks,
                'oven1' : database_form.oven1,
                'time1' : database_form.time1,
                'source1' : database_form.source1,
                'comments1' : database_form.comments1,
            }
            form = formE_form(initial=initial_data)

            if request.method == "POST":
                check = formE_form(request.POST)
                A_valid = check.is_valid()

                if A_valid:
                    A = check.save()

                    if A.leaks == "Yes":
                        issue_page = '../../issues_view/E/' + str(database_form.date) + '/form'

                        return redirect (issue_page)

                    done = Forms.objects.filter(form='E')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()


                    return redirect('IncompleteForms')

        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name,
                'crew' : todays_log.crew,
                'foreman' : todays_log.foreman,
            }
            form = formE_form(initial=initial_data)
            done = Forms.objects.filter(form='E')[0]
            if request.method == "POST":
                check = formE_form(request.POST)
                A_valid = check.is_valid()

                if A_valid:
                    A = check.save()

                    if A.leaks == "Yes":
                        issue_page = '../../issues_view/E/' + str(todays_log.date_save) + '/form'

                        return redirect (issue_page)

                    done = Forms.objects.filter(form='E')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()


                    return redirect('IncompleteForms')
    else:
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name,
            'crew' : todays_log.crew,
            'foreman' : todays_log.foreman,
        }
        form = formE_form(initial=initial_data)
        done = Forms.objects.filter(form='E')[0]
        if request.method == "POST":
            check = formE_form(request.POST)
            A_valid = check.is_valid()
            
            if A_valid:
                A = check.save()

                if A.leaks == "Yes":
                    issue_page = '../../issues_view/E/' + str(todays_log.date_save) + '/form'

                    return redirect (issue_page)
                
                done = Forms.objects.filter(form='E')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()


                return redirect('IncompleteForms')
            
    return render (request, "Daily/formE.html", {
        "back": back, 'todays_log': todays_log, 'form': form, 'selector': selector, 'profile': profile,
    })

#----------------------------------------------------------------------FORM G1---------------<


@lock
def formF1(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    form_all = formF1_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    
    if form_all == 0 :
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name,
            'retain_date' : todays_log.date_save + relativedelta(years=5)
        }
        data = formF1_form(initial=initial_data)
        if request.method == "POST":
            form = formF1_form(request.POST)
            if form.is_valid():
                
                form.save()

                done = Forms.objects.filter(form='F-1')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            
                return redirect('IncompleteForms')
            
    else:
        if today.weekday() not in {0, 1, 5, 6}:
            org = formF1_model.objects.all().order_by('-date')
            database_form = org[0]
            if today.weekday() == 2 :
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                    }
                    data = formF1_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF1_form(request.POST, instance= database_form)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-1')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name,
                        'retain_date' : todays_log.date_save + relativedelta(years=5)
                    }
                    data = formF1_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF1_form(request.POST)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-1')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                if today.weekday() in {3, 4}:
                    last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                    if last_wed == database_form.date:
                        initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                        }
                        data = formF1_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF1_form(request.POST, instance= database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-1')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name,
                            'retain_date' : todays_log.date_save + relativedelta(years=5)
                        }
                        data = formF1_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF1_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-1')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name,
                'retain_date' : todays_log.date_save + relativedelta(years=5)
            }
            data = formF1_form(initial=initial_data)
            if request.method == "POST":
                form = formF1_form(request.POST)
                if form.is_valid():
                    form.save()

                    done = Forms.objects.filter(form='F-1')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    
    return render (request, "Weekly/formF1.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector':selector, 'profile': profile,
    })

@lock
def formF2(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    form_all = formF2_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    
    if form_all == 0 :
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name
        }
        data = formF2_form(initial=initial_data)
        if request.method == "POST":
            form = formF2_form(request.POST)
            if form.is_valid():
                
                form.save()

                done = Forms.objects.filter(form='F-2')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            
                return redirect('IncompleteForms')
            
    else:
        if today.weekday() not in {0, 1, 5, 6}:
            org = formF2_model.objects.all().order_by('-date')
            database_form = org[0]
            if today.weekday() == 2 :
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                    }
                    data = formF2_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF2_form(request.POST, instance= database_form)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-2')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name
                    }
                    data = formF2_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF2_form(request.POST)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-2')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                if today.weekday() in {3, 4}:
                    last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                    if last_wed == database_form.date:
                        initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                        }
                        data = formF2_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF2_form(request.POST, instance= database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-2')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name
                        }
                        data = formF2_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF2_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-2')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name
            }
            data = formF2_form(initial=initial_data)
            if request.method == "POST":
                form = formF2_form(request.POST)
                if form.is_valid():
                    form.save()

                    done = Forms.objects.filter(form='F-2')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    
    return render (request, "Weekly/formF2.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector':selector, 'profile': profile,
    })

@lock
def formF3(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    form_all = formF3_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    
    if form_all == 0 :
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name
        }
        data = formF3_form(initial=initial_data)
        if request.method == "POST":
            form = formF3_form(request.POST)
            if form.is_valid():
                
                form.save()

                done = Forms.objects.filter(form='F-3')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            
                return redirect('IncompleteForms')
            
    else:
        if today.weekday() not in {0, 1, 5, 6}:
            org = formF3_model.objects.all().order_by('-date')
            database_form = org[0]
            if today.weekday() == 2 :
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                    }
                    data = formF3_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF3_form(request.POST, instance= database_form)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-3')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name
                    }
                    data = formF3_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF3_form(request.POST)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-3')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                if today.weekday() in {3, 4}:
                    last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                    if last_wed == database_form.date:
                        initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                        }
                        data = formF3_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF3_form(request.POST, instance= database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-3')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name
                        }
                        data = formF3_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF3_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-3')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name
            }
            data = formF3_form(initial=initial_data)
            if request.method == "POST":
                form = formF3_form(request.POST)
                if form.is_valid():
                    form.save()

                    done = Forms.objects.filter(form='F-3')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    
    return render (request, "Weekly/formF3.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector':selector, 'profile': profile,
    })

@lock
def formF4(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    form_all = formF4_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    
    if form_all == 0 :
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name
        }
        data = formF4_form(initial=initial_data)
        if request.method == "POST":
            form = formF4_form(request.POST)
            if form.is_valid():
                
                form.save()

                done = Forms.objects.filter(form='F-4')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            
                return redirect('IncompleteForms')
            
    else:
        if today.weekday() not in {0, 1, 5, 6}:
            org = formF4_model.objects.all().order_by('-date')
            database_form = org[0]
            if today.weekday() == 2 :
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                    }
                    data = formF4_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF4_form(request.POST, instance= database_form)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-4')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name
                    }
                    data = formF4_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF4_form(request.POST)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-4')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                if today.weekday() in {3, 4}:
                    last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                    if last_wed == database_form.date:
                        initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                        }
                        data = formF4_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF4_form(request.POST, instance= database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-4')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name
                        }
                        data = formF4_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF4_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-4')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name
            }
            data = formF4_form(initial=initial_data)
            if request.method == "POST":
                form = formF4_form(request.POST)
                if form.is_valid():
                    form.save()

                    done = Forms.objects.filter(form='F-4')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    
    return render (request, "Weekly/formF4.html", {
        "back": back, 'todays_log': todays_log, 'data': data, "today" :today, 'selector':selector, 'profile': profile,
    })
@lock
def formF5(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    form_all = formF5_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    
    if form_all == 0 :
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name
        }
        data = formF5_form(initial=initial_data)
        if request.method == "POST":
            form = formF5_form(request.POST)
            if form.is_valid():
                
                form.save()

                done = Forms.objects.filter(form='F-5')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            
                return redirect('IncompleteForms')
            
    else:
        if today.weekday() not in {0, 1, 5, 6}:
            org = formF5_model.objects.all().order_by('-date')
            database_form = org[0]
            if today.weekday() == 2 :
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                    }
                    data = formF5_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF5_form(request.POST, instance= database_form)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-5')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name
                    }
                    data = formF5_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF5_form(request.POST)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-5')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                if today.weekday() in {3, 4}:
                    last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                    if last_wed == database_form.date:
                        initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                        }
                        data = formF5_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF5_form(request.POST, instance= database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-5')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name
                        }
                        data = formF5_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF5_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-5')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name
            }
            data = formF5_form(initial=initial_data)
            if request.method == "POST":
                form = formF5_form(request.POST)
                if form.is_valid():
                    form.save()

                    done = Forms.objects.filter(form='F-5')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    
    return render (request, "Weekly/formF5.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector':selector, 'profile': profile,
    })
@lock
def formF6(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    form_all = formF6_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    
    if form_all == 0 :
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name
        }
        data = formF6_form(initial=initial_data)
        if request.method == "POST":
            form = formF6_form(request.POST)
            if form.is_valid():
                
                form.save()

                done = Forms.objects.filter(form='F-6')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            
                return redirect('IncompleteForms')
            
    else:
        if today.weekday() not in {0, 1, 5, 6}:
            org = formF6_model.objects.all().order_by('-date')
            database_form = org[0]
            if today.weekday() == 2 :
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                    }
                    data = formF6_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF6_form(request.POST, instance= database_form)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-6')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name
                    }
                    data = formF6_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF6_form(request.POST)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-6')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                if today.weekday() in {3, 4}:
                    last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                    if last_wed == database_form.date:
                        initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                        }
                        data = formF6_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF6_form(request.POST, instance= database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-6')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name
                        }
                        data = formF6_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF6_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-6')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name
            }
            data = formF6_form(initial=initial_data)
            if request.method == "POST":
                form = formF6_form(request.POST)
                if form.is_valid():
                    form.save()

                    done = Forms.objects.filter(form='F-6')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    
    return render (request, "Weekly/formF6.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector':selector, 'profile': profile,
    })
@lock
def formF7(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    form_all = formF7_model.objects.count()
    
    full_name = request.user.get_full_name()
    
    
    if form_all == 0 :
        initial_data = {
            'date' : todays_log.date_save,
            'observer' : full_name
        }
        data = formF7_form(initial=initial_data)
        if request.method == "POST":
            form = formF7_form(request.POST)
            if form.is_valid():
                
                form.save()

                done = Forms.objects.filter(form='F-7')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            
                return redirect('IncompleteForms')
            
    else:
        if today.weekday() not in {0, 1, 5, 6}:
            org = formF7_model.objects.all().order_by('-date')
            database_form = org[0]
            if today.weekday() == 2 :
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'status_7' : database_form.status_7,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'comments_7' : database_form.comments_7,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'action_7' : database_form.action_7,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                    }
                    data = formF7_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF7_form(request.POST, instance= database_form)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-7')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'observer' : full_name
                    }
                    data = formF7_form(initial=initial_data)
                    if request.method == "POST":
                        form = formF7_form(request.POST)
                        if form.is_valid():
                            form.save()

                            done = Forms.objects.filter(form='F-7')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                if today.weekday() in {3, 4}:
                    last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                    if last_wed == database_form.date:
                        initial_data = {
                        'observer' : database_form.observer,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'retain_date' : database_form.retain_date,
                        'status_1' : database_form.status_1,
                        'status_2' : database_form.status_2,
                        'status_3' : database_form.status_3,
                        'status_4' : database_form.status_4,
                        'status_5' : database_form.status_5,
                        'status_6' : database_form.status_6,
                        'comments_1' : database_form.comments_1,
                        'comments_2' : database_form.comments_2,
                        'comments_3' : database_form.comments_3,
                        'comments_4' : database_form.comments_4,
                        'comments_5' : database_form.comments_5,
                        'comments_6' : database_form.comments_6,
                        'action_1' : database_form.action_1,
                        'action_2' : database_form.action_2,
                        'action_3' : database_form.action_3,
                        'action_4' : database_form.action_4,
                        'action_5' : database_form.action_5,
                        'action_6' : database_form.action_6,
                        'waste_des_1' : database_form.waste_des_1,
                        'waste_des_2' : database_form.waste_des_2,
                        'waste_des_3' : database_form.waste_des_3,
                        'waste_des_4' : database_form.waste_des_4,
                        'containers_1' : database_form.containers_1,
                        'containers_2' : database_form.containers_2,
                        'containers_3' : database_form.containers_3,
                        'containers_4' : database_form.containers_4,
                        'waste_codes_1' : database_form.waste_codes_1,
                        'waste_codes_2' : database_form.waste_codes_2,
                        'waste_codes_3' : database_form.waste_codes_3,
                        'waste_codes_4' : database_form.waste_codes_4,
                        'dates_1' : database_form.dates_1,
                        'dates_2' : database_form.dates_2,
                        'dates_3' : database_form.dates_3,
                        'dates_4' : database_form.dates_4,
                        }
                        data = formF7_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF7_form(request.POST, instance= database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-7')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name
                        }
                        data = formF7_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF7_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-7')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'observer' : full_name
            }
            data = formF7_form(initial=initial_data)
            if request.method == "POST":
                form = formF7_form(request.POST)
                if form.is_valid():
                    form.save()

                    done = Forms.objects.filter(form='F-7')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
    
    return render (request, "Weekly/formF7.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector':selector, 'profile': profile,
    })

@lock
def formG1(request, selector):
    profile = user_profile_model.objects.all()
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
        'process_equip1' : "-",
        'process_equip2' : "-",
        'op_mode1' : "normal",
        'op_mode2' : "normal",
        'emission_point_start' : "Above Stack",
        'emission_point_stop' : "Same",
        'height_above_ground' : "150",
        'height_rel_observer' : "150",
        'water_drolet_present' : "No",
        'water_droplet_plume' : "N/A",
        'describe_background_start' : "Skies",
        'describe_background_stop' : "Same"
    }
    data = formG1_form(initial=initial_data)
    profile_form = user_profile_form()
    readings_form = formA5_readings_form()
    
    if request.method == "POST":
        form = formG1_form(request.POST)
        
        A_valid = form.is_valid()
        
        if A_valid:
            A = form.save()
            
            done = Forms.objects.filter(form='G-1')[0]
            done.submitted = True
            done.save()
            
            return redirect('IncompleteForms')
    else:
        form = formG1_form(initial=initial_data)
        
    return render (request, "Weekly/formG1.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'profile_form': profile_form,  'selector':selector, 'profile': profile,
    })

@lock
def formG2(request, selector):
    profile = user_profile_model.objects.all()
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
        'process_equip1' : "-",
        'process_equip2' : "-",
        'op_mode1' : "normal",
        'op_mode2' : "normal",
        'emission_point_start' : "Above Stack",
        'emission_point_stop' : "Same",
        'height_above_ground' : "150",
        'height_rel_observer' : "150",
        'water_drolet_present' : "No",
        'water_droplet_plume' : "N/A",
        'describe_background_start' : "Skies",
        'describe_background_stop' : "Same"
    }
    data = formG2_form
    profile_form = user_profile_form()
    readings_form = formA5_readings_form()
    
    if request.method == "POST":
        form = formG2_form(request.POST)
        
        A_valid = form.is_valid()
        
        if A_valid:
            A = form.save()
            
            done = Forms.objects.filter(form='G-1')[0]
            done.submitted = True
            done.save()
            
            return redirect('IncompleteForms')
    else:
        form = formG2_form(initial=initial_data)
        
    return render (request, "Monthly/formG2.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'profile_form': profile_form,  'selector':selector, 'profile': profile,
    })


#----------------------------------------------------------------------FORM H---------------<
@lock
def formH(request, access_page):
    profile = user_profile_model.objects.all()
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    
    org = formH_model.objects.all().order_by('-date')
    
    if access_page != 'form':
        for x in org:
            if str(x.date) == str(access_page):
                database_model = x
        data = database_model
        profile_form = ''
    else:
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
            'process_equip1' : "-",
            'process_equip2' : "-",
            'op_mode1' : "normal",
            'op_mode2' : "normal",
            'emission_point_start' : "Above Stack",
            'emission_point_stop' : "Same",
            'height_above_ground' : "300",
            'height_rel_observer' : "300",
            'water_drolet_present' : "No",
            'water_droplet_plume' : "N/A",
            'describe_background_start' : "Skies",
            'describe_background_stop' : "Same"
        }
        data = formH_form(initial=initial_data)
        profile_form = user_profile_form()
        readings_form = formA5_readings_form()

        if request.method == "POST":
            form = formH_form(request.POST)

            A_valid = form.is_valid()

            if A_valid:
                A = form.save()

                done = Forms.objects.filter(form='H')[0]
                done.submitted = True
                done.save()

                return redirect('IncompleteForms')
        else:
            form = formH_form(initial=initial_data)
        
    return render (request, "Weekly/formH.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'profile_form': profile_form, 'access_page': access_page, 'profile': profile,
    })

#----------------------------------------------------------------------FORM I---------------<
@lock
def formI(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_saturday + one_week
    today_number = today.weekday()
    
    week_start_dates = formI_model.objects.all().order_by('-week_start')
    week_almost = week_start_dates[0]
    week = week_almost.week_start
    opened = True
    submit = True
    
    if selector not in ('form', 'edit'):
        submit = False
        for x in week_start_dates:
            if str(x.week_start) == str(selector):
                database_model = x
        empty_form = database_model
    else:
        if today.weekday() not in {5, 6}:
            home = []
            filled_in = False
            for x in formI_model.objects.all():
                if x.week_start == last_saturday:
                    home.append((x.time_4, 4))
                    home.append((x.time_3, 3))
                    home.append((x.time_2, 2))
                    home.append((x.time_1, 1))
                    home.append((x.time_0, 0))

            for days in home:
                if days[0]:
                    if days[1] == today_number:
                        filled_in = True
            
            if selector == 'form':
                if week == last_saturday:
                    if filled_in:
                        empty_form = week_almost
                        submit = False
                    else:
                        initial_data = {
                            'week_start' : week_almost.week_start,
                            'week_end' : week_almost.week_end,
                            'time_0' : week_almost.time_0,
                            'time_1' : week_almost.time_1,
                            'time_2' : week_almost.time_2,
                            'time_3' : week_almost.time_3,
                            'time_4' : week_almost.time_4,
                            'obser_0' : week_almost.obser_0,
                            'obser_1' : week_almost.obser_1,
                            'obser_2' : week_almost.obser_2,
                            'obser_3' : week_almost.obser_3,
                            'obser_4' : week_almost.obser_4,
                        }

                        empty_form = formI_form(initial=initial_data)
                        if request.method == "POST":
                            form = formI_form(request.POST, instance= week_almost)
                            A_valid = form.is_valid()
                            if A_valid:
                                form.save()

                                B = []
                                for x in formI_model.objects.all():
                                    if x.week_start == last_saturday:
                                        B.append((4, x.time_4, x.obser_4))
                                        B.append((3, x.time_3, x.obser_3))
                                        B.append((2, x.time_2, x.obser_2))
                                        B.append((1, x.time_1, x.obser_1))
                                        B.append((0, x.time_0, x.obser_0))

                                for days in B:
                                    if days[0] == today_number:
                                        if days[1] and days[2]:
                                            filled_in = True
                                        else:
                                            filled_in = False

                                if filled_in:
                                    done = Forms.objects.filter(form='I')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')

                else:
                    initial_data = {
                        'week_start' : last_saturday,
                        'week_end' : end_week
                    }

                    empty_form = formI_form(initial= initial_data)
                    if request.method == "POST":
                        form = formI_form(request.POST)
                        A_valid = form.is_valid()
                        if A_valid:
                            form.save()

                            done = Forms.objects.filter(form='I')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                        
        #-------EDIT--------EDIT -------- EDIT-------                
        #-------EDIT--------EDIT -------- EDIT-------                
        #-------EDIT--------EDIT -------- EDIT-------
            elif selector == 'edit':
                filled_in = False
                initial_data = {
                    'week_start' : week_almost.week_start,
                    'week_end' : week_almost.week_end,
                    'time_0' : week_almost.time_0,
                    'time_1' : week_almost.time_1,
                    'time_2' : week_almost.time_2,
                    'time_3' : week_almost.time_3,
                    'time_4' : week_almost.time_4,
                    'obser_0' : week_almost.obser_0,
                    'obser_1' : week_almost.obser_1,
                    'obser_2' : week_almost.obser_2,
                    'obser_3' : week_almost.obser_3,
                    'obser_4' : week_almost.obser_4,
                }

                empty_form = formI_form(initial=initial_data)
                if request.method == "POST":
                    form = formI_form(request.POST, instance= week_almost)
                    A_valid = form.is_valid()
                    if A_valid:
                        form.save()

                        B = []
                        for x in formI_model.objects.all():
                            if x.week_start == last_saturday:
                                B.append((4, x.time_4, x.obser_4))
                                B.append((3, x.time_3, x.obser_3))
                                B.append((2, x.time_2, x.obser_2))
                                B.append((1, x.time_1, x.obser_1))
                                B.append((0, x.time_0, x.obser_0))

                        for days in B:
                            if days[0] == today_number:
                                if days[1] and days[2]:
                                    filled_in = True
                                else:
                                    filled_in = False

                        if filled_in:
                            done = Forms.objects.filter(form='I')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
        elif today.weekday() == 5:
            opened = False
            submit = False
            initial_data = {
                'week_start' : today,
                'week_end' : today + one_week
            }

            empty_form = formI_form(initial= initial_data)

        else:
            opened = False
            submit = False
            initial_data = {
                'week_start' : today - datetime.timedelta(days=1),
                'week_end' : today + one_week
            }

            empty_form = formI_form(initial= initial_data)

        
    return render (request, "Daily/formI.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'week': week, 'opened': opened, 'week_almost': week_almost, 'end_week': end_week, 'selector':selector, 'profile': profile, 'submit': submit, 'filled_in': filled_in
    })

#----------------------------------------------------------------------FORM L---------------<
@lock
def formL(request, access_page):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_saturday + one_week
    today_number = today.weekday()
    
    week_start_dates = formL_model.objects.all().order_by('-week_start')
    week_almost = week_start_dates[0]
    this_week_saturday = week_almost.week_start
    database = week_almost
    opened = True
    
    if access_page not in ('form', 'edit'):
        for x in week_start_dates:
            if str(x.week_start) == str(access_page):
                database_model = x
                filled_in = True
        empty_form = database_model
    else:
        if today.weekday() not in {5, 6}:
            home = []
            filled_in = False
            for x in formL_model.objects.all():
                if x.week_start == last_saturday:
                    home.append((x.time_4, 4))
                    home.append((x.time_3, 3))
                    home.append((x.time_2, 2))
                    home.append((x.time_1, 1))
                    home.append((x.time_0, 0))
                    home.append((x.time_6, 6))
                    home.append((x.time_5, 5))

            for days in home:
               
                if days[0]:
                    if days[1] == today_number:
                        filled_in = True
    
            if formL_model.objects.count() == 0 :
                empty_form = formL_form()
                if request.method == "POST":
                    form = formL_form(request.POST)
                    A_valid = form.is_valid()
                    if A_valid:
                        A = form.save()

                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                            return redirect('../formH/formL')


                        done = Forms.objects.filter(form='L')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
            else:
                if access_page == 'form':
                    if today_number in {0, 1, 2, 3, 4}:
                        if this_week_saturday == last_saturday:
                            if filled_in:
                                empty_form = database
                          
                            else:
                                initial_data = {
                                    'week_start' : database.week_start,
                                    'week_end' : database.week_end,
                                    'time_0' : database.time_0,
                                    'obser_0' : database.obser_0,
                                    'vents_0' : database.vents_0,
                                    'mixer_0' : database.mixer_0,
                                    'v_comments_0' : database.v_comments_0,
                                    'm_comments_0' : database.m_comments_0,
                                    'time_1' : database.time_1,
                                    'obser_1' : database.obser_1,
                                    'vents_1' : database.vents_1,
                                    'mixer_1' : database.mixer_1,
                                    'v_comments_1' : database.v_comments_1,
                                    'm_comments_1' : database.m_comments_1,
                                    'time_2' : database.time_2,
                                    'obser_2' : database.obser_2,
                                    'vents_2' : database.vents_2,
                                    'mixer_2' : database.mixer_2,
                                    'v_comments_2' : database.v_comments_2,
                                    'm_comments_2' : database.m_comments_2,
                                    'time_3' : database.time_3,
                                    'obser_3' : database.obser_3,
                                    'vents_3' : database.vents_3,
                                    'mixer_3' : database.mixer_3,
                                    'v_comments_3' : database.v_comments_3,
                                    'm_comments_3' : database.m_comments_3,
                                    'time_4' : database.time_4,
                                    'obser_4' : database.obser_4,
                                    'vents_4' : database.vents_4,
                                    'mixer_4' : database.mixer_4,
                                    'v_comments_4' : database.v_comments_4,
                                    'm_comments_4' : database.m_comments_4,
                                    'time_5' : database.time_5,
                                    'obser_5' : database.obser_5,
                                    'vents_5' : database.vents_5,
                                    'mixer_5' : database.mixer_5,
                                    'v_comments_5' : database.v_comments_5,
                                    'm_comments_5' : database.m_comments_5,
                                    'time_6' : database.time_6,
                                    'obser_6' : database.obser_6,
                                    'vents_6' : database.vents_6,
                                    'mixer_6' : database.mixer_6,
                                    'v_comments_6' : database.v_comments_6,
                                    'm_comments_6' : database.m_comments_6,
                                }

                                empty_form = formL_form(initial= initial_data)
                                
                                if request.method == "POST":
                                    form = formL_form(request.POST, instance= database)
                                    A_valid = form.is_valid()
                                    if A_valid:

                                        A = form.save()
                                        
                                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                            return redirect('../formH/formL')

                                        B = []
                                        for x in formL_model.objects.all():
                                            
                                            if x.week_start == last_saturday:
                                                B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4 ))
                                                B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3 ))
                                                B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2 ))
                                                B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1 ))
                                                B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0 ))
                                                B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6 ))
                                                B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5 ))
                                        for days in B:
                                       
                                            if days[0] == today_number:
                    
                                                if days[1] and days[2] and days[3] and days[4] and days[5] and days[6]:
                                                    filled_in = True
                                   
                                                else:
                                                    filled_in = False
                                        if filled_in:
                                     
                                            done = Forms.objects.filter(form='L')[0]
                                            done.submitted = True
                                            done.date_submitted = todays_log.date_save
                                            done.save()

                                            return redirect('IncompleteForms')
                                        else:
                                            done = Forms.objects.filter(form='L')[0]
                                            done.submitted = False
                                            done.date_submitted = todays_log.date_save - datetime.timedelta(days=1)
                                            done.save()

                                            return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'week_start' : last_saturday,
                                'week_end' : end_week
                            }
                            empty_form = formL_form(initial= initial_data)
                            if request.method == "POST":
                                form = formL_form(request.POST)
                                A_valid = form.is_valid()
                                if A_valid:
                                    A = form.save()

                                    if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                        return redirect('../formH/formL')

                                    done = Forms.objects.filter(form='L')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                    else:
                        if today_number == 5:
                            if this_week_saturday == today:
                                if  filled_in:
                                    empty_form = database
                                else:
                                    initial_data = {
                                        'week_start' : database.week_start,
                                        'week_end' : database.week_end,
                                        'time_0' : database.time_0,
                                        'obser_0' : database.obser_0,
                                        'vents_0' : database.vents_0,
                                        'mixer_0' : database.mixer_0,
                                        'v_comments_0' : database.v_comments_0,
                                        'm_comments_0' : database.m_comments_0,
                                        'time_1' : database.time_1,
                                        'obser_1' : database.obser_1,
                                        'vents_1' : database.vents_1,
                                        'mixer_1' : database.mixer_1,
                                        'v_comments_1' : database.v_comments_1,
                                        'm_comments_1' : database.m_comments_1,
                                        'time_2' : database.time_2,
                                        'obser_2' : database.obser_2,
                                        'vents_2' : database.vents_2,
                                        'mixer_2' : database.mixer_2,
                                        'v_comments_2' : database.v_comments_2,
                                        'm_comments_2' : database.m_comments_2,
                                        'time_3' : database.time_3,
                                        'obser_3' : database.obser_3,
                                        'vents_3' : database.vents_3,
                                        'mixer_3' : database.mixer_3,
                                        'v_comments_3' : database.v_comments_3,
                                        'm_comments_3' : database.m_comments_3,
                                        'time_4' : database.time_4,
                                        'obser_4' : database.obser_4,
                                        'vents_4' : database.vents_4,
                                        'mixer_4' : database.mixer_4,
                                        'v_comments_4' : database.v_comments_4,
                                        'm_comments_4' : database.m_comments_4,
                                        'time_5' : database.time_5,
                                        'obser_5' : database.obser_5,
                                        'vents_5' : database.vents_5,
                                        'mixer_5' : database.mixer_5,
                                        'v_comments_5' : database.v_comments_5,
                                        'm_comments_5' : database.m_comments_5,
                                        'time_6' : database.time_6,
                                        'obser_6' : database.obser_6,
                                        'vents_6' : database.vents_6,
                                        'mixer_6' : database.mixer_6,
                                        'v_comments_6' : database.v_comments_6,
                                        'm_comments_6' : database.m_comments_6,
                                    }

                                    empty_form = formL_form(initial= initial_data)
                                    if request.method == "POST":
                                        form = formL_form(request.POST, instance= database)
                                        A_valid = form.is_valid()
                                        if A_valid:
                                            A = form.save()

                                            if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                                return redirect('../formH/formL')

                                            B = []
                                            for x in formL_model.objects.all():
                                                if x.week_start == last_saturday:
                                                    B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4 ))
                                                    B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3 ))
                                                    B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2 ))
                                                    B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1 ))
                                                    B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0 ))
                                                    B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6 ))
                                                    B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5 ))
                                            for days in B:
                                                if days[0] == today_number:
                                                    if days[1] and days[2] and days[3] and days[4] and days[5] and days[6]:
                                                        filled_in = True
                                                    else:
                                                        filled_in = False
                                            if filled_in:
                                                done = Forms.objects.filter(form='L')[0]
                                                done.submitted = True
                                                done.date_submitted = todays_log.date_save
                                                done.save()

                                                return redirect('IncompleteForms')
                                            else:
                                                done = Forms.objects.filter(form='L')[0]
                                                done.submitted = False
                                                done.date_submitted = todays_log.date_save - datetime.timedelta(days=1)
                                                done.save()

                                                return redirect('IncompleteForms')
                            else:
                                initial_data = {
                                    'week_start' : last_saturday,
                                    'week_end' : end_week
                                }
                                empty_form = formL_form(initial= initial_data)
                                if request.method == "POST":
                                    form = formL_form(request.POST)
                                    A_valid = form.is_valid()
                                    if A_valid:
                                        A = form.save()

                                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                            return redirect('../formH/formL')

                                        done = Forms.objects.filter(form='L')[0]
                                        done.submitted = True
                                        done.date_submitted = todays_log.date_save
                                        done.save()

                                        return redirect('IncompleteForms')    
                        else:
                            sunday_last_sat = today - datetime.timedelta(days=1)
                            if this_week_saturday == sunday_last_sat:
                                if  filled_in:
                                    empty_form = database
                                else:
                                    initial_data = {
                                        'week_start' : database.week_start,
                                        'week_end' : database.week_end,
                                        'time_0' : database.time_0,
                                        'obser_0' : database.obser_0,
                                        'vents_0' : database.vents_0,
                                        'mixer_0' : database.mixer_0,
                                        'v_comments_0' : database.v_comments_0,
                                        'm_comments_0' : database.m_comments_0,
                                        'time_1' : database.time_1,
                                        'obser_1' : database.obser_1,
                                        'vents_1' : database.vents_1,
                                        'mixer_1' : database.mixer_1,
                                        'v_comments_1' : database.v_comments_1,
                                        'm_comments_1' : database.m_comments_1,
                                        'time_2' : database.time_2,
                                        'obser_2' : database.obser_2,
                                        'vents_2' : database.vents_2,
                                        'mixer_2' : database.mixer_2,
                                        'v_comments_2' : database.v_comments_2,
                                        'm_comments_2' : database.m_comments_2,
                                        'time_3' : database.time_3,
                                        'obser_3' : database.obser_3,
                                        'vents_3' : database.vents_3,
                                        'mixer_3' : database.mixer_3,
                                        'v_comments_3' : database.v_comments_3,
                                        'm_comments_3' : database.m_comments_3,
                                        'time_4' : database.time_4,
                                        'obser_4' : database.obser_4,
                                        'vents_4' : database.vents_4,
                                        'mixer_4' : database.mixer_4,
                                        'v_comments_4' : database.v_comments_4,
                                        'm_comments_4' : database.m_comments_4,
                                        'time_5' : database.time_5,
                                        'obser_5' : database.obser_5,
                                        'vents_5' : database.vents_5,
                                        'mixer_5' : database.mixer_5,
                                        'v_comments_5' : database.v_comments_5,
                                        'm_comments_5' : database.m_comments_5,
                                        'time_6' : database.time_6,
                                        'obser_6' : database.obser_6,
                                        'vents_6' : database.vents_6,
                                        'mixer_6' : database.mixer_6,
                                        'v_comments_6' : database.v_comments_6,
                                        'm_comments_6' : database.m_comments_6,
                                    }

                                    empty_form = formL_form(initial= initial_data)
                                    if request.method == "POST":
                                        form = formL_form(request.POST, instance= database)
                                        A_valid = form.is_valid()
                                        if A_valid:
                                            A = form.save()

                                            if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                                return redirect('../formH/formL')

                                            B = []
                                            for x in formL_model.objects.all():
                                                if x.week_start == last_saturday:
                                                    B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4 ))
                                                    B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3 ))
                                                    B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2 ))
                                                    B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1 ))
                                                    B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0 ))
                                                    B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6 ))
                                                    B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5 ))
                                            for days in B:
                                                if days[0] == today_number:
                                                    if days[1] and days[2] and days[3] and days[4] and days[5] and days[6]:
                                                        filled_in = True
                                                    else:
                                                        filled_in = False
                                            if filled_in:
                                                done = Forms.objects.filter(form='L')[0]
                                                done.submitted = True
                                                done.date_submitted = todays_log.date_save
                                                done.save()

                                                return redirect('IncompleteForms')
                                            else:
                                                done = Forms.objects.filter(form='L')[0]
                                                done.submitted = False
                                                done.date_submitted = todays_log.date_save - datetime.timedelta(days=1)
                                                done.save()

                                                return redirect('IncompleteForms')
                            else:
                                initial_data = {
                                    'week_start' : last_saturday,
                                    'week_end' : end_week
                                }
                                empty_form = formL_form(initial= initial_data)
                                if request.method == "POST":
                                    form = formL_form(request.POST)
                                    A_valid = form.is_valid()
                                    if A_valid:
                                        A = form.save()

                                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                            return redirect('../formH/formL')

                                        done = Forms.objects.filter(form='L')[0]
                                        done.submitted = True
                                        done.date_submitted = todays_log.date_save
                                        done.save()

                                        return redirect('IncompleteForms')  
           #----------------EDIT-------------EDIT---------EDIT---------------  
        #----------------EDIT-------------EDIT---------EDIT---------------
        #----------------EDIT-------------EDIT---------EDIT---------------
        #----------------EDIT-------------EDIT---------EDIT---------------
        #----------------EDIT-------------EDIT---------EDIT---------------
        #----------------EDIT-------------EDIT---------EDIT---------------
                if access_page == "edit":
                    filled_in = False
                    if today_number in {0, 1, 2, 3, 4}:
                        if this_week_saturday == last_saturday:
                            initial_data = {
                                'week_start' : database.week_start,
                                'week_end' : database.week_end,
                                'time_0' : database.time_0,
                                'obser_0' : database.obser_0,
                                'vents_0' : database.vents_0,
                                'mixer_0' : database.mixer_0,
                                'v_comments_0' : database.v_comments_0,
                                'm_comments_0' : database.m_comments_0,
                                'time_1' : database.time_1,
                                'obser_1' : database.obser_1,
                                'vents_1' : database.vents_1,
                                'mixer_1' : database.mixer_1,
                                'v_comments_1' : database.v_comments_1,
                                'm_comments_1' : database.m_comments_1,
                                'time_2' : database.time_2,
                                'obser_2' : database.obser_2,
                                'vents_2' : database.vents_2,
                                'mixer_2' : database.mixer_2,
                                'v_comments_2' : database.v_comments_2,
                                'm_comments_2' : database.m_comments_2,
                                'time_3' : database.time_3,
                                'obser_3' : database.obser_3,
                                'vents_3' : database.vents_3,
                                'mixer_3' : database.mixer_3,
                                'v_comments_3' : database.v_comments_3,
                                'm_comments_3' : database.m_comments_3,
                                'time_4' : database.time_4,
                                'obser_4' : database.obser_4,
                                'vents_4' : database.vents_4,
                                'mixer_4' : database.mixer_4,
                                'v_comments_4' : database.v_comments_4,
                                'm_comments_4' : database.m_comments_4,
                                'time_5' : database.time_5,
                                'obser_5' : database.obser_5,
                                'vents_5' : database.vents_5,
                                'mixer_5' : database.mixer_5,
                                'v_comments_5' : database.v_comments_5,
                                'm_comments_5' : database.m_comments_5,
                                'time_6' : database.time_6,
                                'obser_6' : database.obser_6,
                                'vents_6' : database.vents_6,
                                'mixer_6' : database.mixer_6,
                                'v_comments_6' : database.v_comments_6,
                                'm_comments_6' : database.m_comments_6,
                            }

                            empty_form = formL_form(initial= initial_data)

                            if request.method == "POST":
                                form = formL_form(request.POST, instance= database)
                                A_valid = form.is_valid()
                                if A_valid:
                                    A = form.save()

                                    if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                        return redirect('../formH/formL')

                                    B = []
                                    for x in formL_model.objects.all():
                                        if x.week_start == last_saturday:
                                            B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4 ))
                                            B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3 ))
                                            B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2 ))
                                            B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1 ))
                                            B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0 ))
                                            B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6 ))
                                            B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5 ))
                                    for days in B:
                                        if days[0] == today_number:
                                            if days[1] and days[2] and days[3] and days[4] and days[5] and days[6]:
                                                filled_in = True
                                            else:
                                                filled_in = False
                                    if filled_in:
                                        print('chicken')
                                        done = Forms.objects.filter(form='L')[0]
                                        done.submitted = True
                                        done.date_submitted = todays_log.date_save
                                        done.save()

                                        return redirect('IncompleteForms')
                                    else:
                                        done = Forms.objects.filter(form='L')[0]
                                        done.submitted = False
                                        done.date_submitted = todays_log.date_save - datetime.timedelta(days=1)
                                        done.save()

                                        return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'week_start' : last_saturday,
                                'week_end' : end_week
                            }
                            empty_form = formL_form(initial= initial_data)
                            if request.method == "POST":
                                form = formL_form(request.POST)
                                A_valid = form.is_valid()
                                if A_valid:
                                    A = form.save()

                                    if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                        return redirect('../formH/formL')

                                    done = Forms.objects.filter(form='L')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                    else:
                        if today_number == 5:
                            if this_week_saturday == today:
                                initial_data = {
                                    'week_start' : database.week_start,
                                    'week_end' : database.week_end,
                                    'time_0' : database.time_0,
                                    'obser_0' : database.obser_0,
                                    'vents_0' : database.vents_0,
                                    'mixer_0' : database.mixer_0,
                                    'v_comments_0' : database.v_comments_0,
                                    'm_comments_0' : database.m_comments_0,
                                    'time_1' : database.time_1,
                                    'obser_1' : database.obser_1,
                                    'vents_1' : database.vents_1,
                                    'mixer_1' : database.mixer_1,
                                    'v_comments_1' : database.v_comments_1,
                                    'm_comments_1' : database.m_comments_1,
                                    'time_2' : database.time_2,
                                    'obser_2' : database.obser_2,
                                    'vents_2' : database.vents_2,
                                    'mixer_2' : database.mixer_2,
                                    'v_comments_2' : database.v_comments_2,
                                    'm_comments_2' : database.m_comments_2,
                                    'time_3' : database.time_3,
                                    'obser_3' : database.obser_3,
                                    'vents_3' : database.vents_3,
                                    'mixer_3' : database.mixer_3,
                                    'v_comments_3' : database.v_comments_3,
                                    'm_comments_3' : database.m_comments_3,
                                    'time_4' : database.time_4,
                                    'obser_4' : database.obser_4,
                                    'vents_4' : database.vents_4,
                                    'mixer_4' : database.mixer_4,
                                    'v_comments_4' : database.v_comments_4,
                                    'm_comments_4' : database.m_comments_4,
                                    'time_5' : database.time_5,
                                    'obser_5' : database.obser_5,
                                    'vents_5' : database.vents_5,
                                    'mixer_5' : database.mixer_5,
                                    'v_comments_5' : database.v_comments_5,
                                    'm_comments_5' : database.m_comments_5,
                                    'time_6' : database.time_6,
                                    'obser_6' : database.obser_6,
                                    'vents_6' : database.vents_6,
                                    'mixer_6' : database.mixer_6,
                                    'v_comments_6' : database.v_comments_6,
                                    'm_comments_6' : database.m_comments_6,
                                }

                                empty_form = formL_form(initial= initial_data)
                                if request.method == "POST":
                                    form = formL_form(request.POST, instance= database)
                                    A_valid = form.is_valid()
                                    if A_valid:
                                        A = form.save()

                                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                            return redirect('../formH/formL')

                                        B = []
                                        for x in formL_model.objects.all():
                                            if x.week_start == last_saturday:
                                                B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4 ))
                                                B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3 ))
                                                B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2 ))
                                                B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1 ))
                                                B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0 ))
                                                B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6 ))
                                                B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5 ))
                                        for days in B:
                                            if days[0] == today_number:
                                                if days[1] and days[2] and days[3] and days[4] and days[5] and days[6]:
                                                    filled_in = True
                                                else:
                                                    filled_in = False
                                        if filled_in:
                                            done = Forms.objects.filter(form='L')[0]
                                            done.submitted = True
                                            done.date_submitted = todays_log.date_save
                                            done.save()

                                            return redirect('IncompleteForms')
                                        else:
                                            done = Forms.objects.filter(form='L')[0]
                                            done.submitted = False
                                            done.date_submitted = todays_log.date_save - datetime.timedelta(days=1)
                                            done.save()

                                            return redirect('IncompleteForms')
                            else:
                                initial_data = {
                                    'week_start' : last_saturday,
                                    'week_end' : end_week
                                }
                                empty_form = formL_form(initial= initial_data)
                                if request.method == "POST":
                                    form = formL_form(request.POST)
                                    A_valid = form.is_valid()
                                    if A_valid:
                                        A = form.save()

                                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                            return redirect('../formH/formL')

                                        done = Forms.objects.filter(form='L')[0]
                                        done.submitted = True
                                        done.date_submitted = todays_log.date_save
                                        done.save()

                                        return redirect('IncompleteForms')    
                        else:
                            sunday_last_sat = today - datetime.timedelta(days=1)
                            if this_week_saturday == sunday_last_sat:
                                initial_data = {
                                    'week_start' : database.week_start,
                                    'week_end' : database.week_end,
                                    'time_0' : database.time_0,
                                    'obser_0' : database.obser_0,
                                    'vents_0' : database.vents_0,
                                    'mixer_0' : database.mixer_0,
                                    'v_comments_0' : database.v_comments_0,
                                    'm_comments_0' : database.m_comments_0,
                                    'time_1' : database.time_1,
                                    'obser_1' : database.obser_1,
                                    'vents_1' : database.vents_1,
                                    'mixer_1' : database.mixer_1,
                                    'v_comments_1' : database.v_comments_1,
                                    'm_comments_1' : database.m_comments_1,
                                    'time_2' : database.time_2,
                                    'obser_2' : database.obser_2,
                                    'vents_2' : database.vents_2,
                                    'mixer_2' : database.mixer_2,
                                    'v_comments_2' : database.v_comments_2,
                                    'm_comments_2' : database.m_comments_2,
                                    'time_3' : database.time_3,
                                    'obser_3' : database.obser_3,
                                    'vents_3' : database.vents_3,
                                    'mixer_3' : database.mixer_3,
                                    'v_comments_3' : database.v_comments_3,
                                    'm_comments_3' : database.m_comments_3,
                                    'time_4' : database.time_4,
                                    'obser_4' : database.obser_4,
                                    'vents_4' : database.vents_4,
                                    'mixer_4' : database.mixer_4,
                                    'v_comments_4' : database.v_comments_4,
                                    'm_comments_4' : database.m_comments_4,
                                    'time_5' : database.time_5,
                                    'obser_5' : database.obser_5,
                                    'vents_5' : database.vents_5,
                                    'mixer_5' : database.mixer_5,
                                    'v_comments_5' : database.v_comments_5,
                                    'm_comments_5' : database.m_comments_5,
                                    'time_6' : database.time_6,
                                    'obser_6' : database.obser_6,
                                    'vents_6' : database.vents_6,
                                    'mixer_6' : database.mixer_6,
                                    'v_comments_6' : database.v_comments_6,
                                    'm_comments_6' : database.m_comments_6,
                                }

                                empty_form = formL_form(initial= initial_data)
                                if request.method == "POST":
                                    form = formL_form(request.POST, instance= database)
                                    A_valid = form.is_valid()
                                    if A_valid:
                                        A = form.save()

                                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                            return redirect('../formH/formL')

                                        B = []
                                        for x in formL_model.objects.all():
                                            if x.week_start == last_saturday:
                                                B.append((4, x.time_4, x.obser_4, x.vents_4, x.mixer_4, x.v_comments_4, x.m_comments_4 ))
                                                B.append((3, x.time_3, x.obser_3, x.vents_3, x.mixer_3, x.v_comments_3, x.m_comments_3 ))
                                                B.append((2, x.time_2, x.obser_2, x.vents_2, x.mixer_2, x.v_comments_2, x.m_comments_2 ))
                                                B.append((1, x.time_1, x.obser_1, x.vents_1, x.mixer_1, x.v_comments_1, x.m_comments_1 ))
                                                B.append((0, x.time_0, x.obser_0, x.vents_0, x.mixer_0, x.v_comments_0, x.m_comments_0 ))
                                                B.append((6, x.time_6, x.obser_6, x.vents_6, x.mixer_6, x.v_comments_6, x.m_comments_6 ))
                                                B.append((5, x.time_5, x.obser_5, x.vents_5, x.mixer_5, x.v_comments_5, x.m_comments_5 ))
                                        for days in B:
                                            if days[0] == today_number:
                                                if days[1] and days[2] and days[3] and days[4] and days[5] and days[6]:
                                                    filled_in = True
                                                else:
                                                    filled_in = False
                                        if filled_in:
                                            done = Forms.objects.filter(form='L')[0]
                                            done.submitted = True
                                            done.date_submitted = todays_log.date_save
                                            done.save()

                                            return redirect('IncompleteForms')
                                        else:
                                            done = Forms.objects.filter(form='L')[0]
                                            done.submitted = False
                                            done.date_submitted = todays_log.date_save - datetime.timedelta(days=1)
                                            done.save()

                                            return redirect('IncompleteForms')
                            else:
                                initial_data = {
                                    'week_start' : last_saturday,
                                    'week_end' : end_week
                                }
                                empty_form = formL_form(initial= initial_data)
                                if request.method == "POST":
                                    form = formL_form(request.POST)
                                    A_valid = form.is_valid()
                                    if A_valid:
                                        A = form.save()

                                        if 'Yes' in {A.vents_0, A.mixer_0, A.vents_1, A.mixer_1, A.vents_2, A.mixer_2, A.vents_3, A.mixer_3, A.vents_4, A.mixer_4, A.vents_5, A.mixer_5, A.vents_6, A.mixer_6 }:
                                            return redirect('../formH/formL')

                                        done = Forms.objects.filter(form='L')[0]
                                        done.submitted = True
                                        done.date_submitted = todays_log.date_save
                                        done.save()

                                        return redirect('IncompleteForms')
        elif today.weekday() == 5:
            opened = False
            filled_in = True
            initial_data = {
                'week_start' : today,
                'week_end' : today + one_week
            }

            empty_form = formI_form(initial= initial_data)

        else:
            opened = False
            submit = True
            initial_data = {
                'week_start' : today - datetime.timedelta(days=1),
                'week_end' : today + one_week
            }

            empty_form = formI_form(initial= initial_data)

            
    return render (request, "Daily/formL.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'this_week_saturday': this_week_saturday, 'last_saturday': last_saturday, 'week_almost': week_almost, 'end_week': end_week, 'filled_in': filled_in, "access_page":access_page, 'profile': profile, 'opened' : opened
    })

#------------------------------------------------------------------------FORM M---------------<
@lock
def formM(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    
    org = formM_model.objects.all().order_by('-date')
    database_form = org[0]
    org2 = formM_readings_model.objects.all().order_by('-form')
    database_form2 = org2[0]
    
    today = datetime.date.today()
    today_number = today.weekday()

    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        form = database_model
    if selector != 'form':
        for x in org2:
            if str(x.form) == str(selector):
                database_model2 = x
            else:
                print('Error - EES_00001')
        form2 = database_model2
    else:
        if selector == 'form':
            if today_number in {0, 1, 2, 3, 4}:
                if todays_log.date_save == database_form.date:
                    initial_data = {
                        'date' : database_form.date,
                        'paved' : database_form.paved,
                        'pav_start' : database_form.pav_start,
                        'pav_stop' : database_form.pav_stop,
                        'unpaved' : database_form.unpaved,
                        'unp_start' : database_form.unp_start,
                        'unp_stop' : database_form.unp_stop,
                        'parking' : database_form.parking,
                        'par_start' : database_form.par_start,
                        'par_stop' : database_form.par_stop,
                        'storage' : database_form.storage,
                        'sto_start' : database_form.sto_start,
                        'sto_stop' : database_form.sto_stop,
                        'observer' : database_form.observer,
                        'cert_date' : database_form.cert_date,
                        'comments' : database_form.comments,
                        
                        'pav_1' : database_form2.pav_1,
                        'pav_2' : database_form2.pav_2,
                        'pav_3' : database_form2.pav_3,
                        'pav_4' : database_form2.pav_4,
                        'pav_5' : database_form2.pav_5,
                        'pav_6' : database_form2.pav_6,
                        'pav_7' : database_form2.pav_7,
                        'pav_8' : database_form2.pav_8,
                        'pav_9' : database_form2.pav_9,
                        'pav_10' : database_form2.pav_10,
                        'pav_11' : database_form2.pav_11,
                        'pav_12' : database_form2.pav_12,
                        'unp_1' : database_form2.unp_1,
                        'unp_2' : database_form2.unp_2,
                        'unp_3' : database_form2.unp_3,
                        'unp_4' : database_form2.unp_4,
                        'unp_5' : database_form2.unp_5,
                        'unp_6' : database_form2.unp_6,
                        'unp_7' : database_form2.unp_7,
                        'unp_8' : database_form2.unp_8,
                        'unp_9' : database_form2.unp_9,
                        'unp_10' : database_form2.unp_10,
                        'unp_11' : database_form2.unp_11,
                        'unp_12' : database_form2.unp_12,
                        'par_1' : database_form2.par_1,
                        'par_2' : database_form2.par_2,
                        'par_3' : database_form2.par_3,
                        'par_4' : database_form2.par_4,
                        'par_5' : database_form2.par_5,
                        'par_6' : database_form2.par_6,
                        'par_7' : database_form2.par_7,
                        'par_8' : database_form2.par_8,
                        'par_9' : database_form2.par_9,
                        'par_10' : database_form2.par_10,
                        'par_11' : database_form2.par_11,
                        'par_12' : database_form2.par_12,
                        'storage_1' : database_form2.storage_1,
                        'storage_2' : database_form2.storage_2,
                        'storage_3' : database_form2.storage_3,
                        'storage_4' : database_form2.storage_4,
                        'storage_5' : database_form2.storage_5,
                        'storage_6' : database_form2.storage_6,
                        'storage_7' : database_form2.storage_7,
                        'storage_8' : database_form2.storage_8,
                        'storage_9' : database_form2.storage_9,
                        'storage_10' : database_form2.storage_10,
                        'storage_11' : database_form2.storage_11,
                        'storage_12' : database_form2.storage_12,
                        
                        'pav_total' : database_form2.pav_total,
                        'unp_total' : database_form2.unp_total,
                        'par_total' : database_form2.par_total,
                        'storage_total' : database_form2.storage_total,
                    }
                    
                    form = formM_form(initial=initial_data)
                    form2 = formM_readings_form(initial=initial_data)
                    
                    if request.method == "POST":
                        form = formM_form(request.POST, instance=database_form)
                        reads = formM_readings_form(request.POST, instance=database_form2)

                        A_valid = form.is_valid()
                        B_valid = reads.is_valid()

                        if A_valid and B_valid:
                            A = form.save()
                            B = reads.save(commit=False)
                            B.form = A
                            B.save()
                            
                            
                            done = Forms.objects.filter(form='M')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()
                            
                            done2 = Forms.objects.filter(form='N')[0]
                            done2.submitted = True
                            done2.date_submitted = todays_log.date_save
                            done2.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                            'date' : todays_log.date_save,
                            'observer' : full_name,
                            'cert_date' : cert_date
                    }
                    form = formM_form(initial=initial_data)
                    form2 = formM_readings_form()
                    
                    if request.method == "POST":
                        form = formM_form(request.POST)
                        reads = formM_readings_form(request.POST)

                        A_valid = form.is_valid()
                        B_valid = reads.is_valid()

                        if A_valid and B_valid:
                            A = form.save()
                            B = reads.save(commit=False)
                            B.form = A
                            B.save()
                            
                            
                            done = Forms.objects.filter(form='M')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()
                            
                            done2 = Forms.objects.filter(form='N')[0]
                            done2.submitted = True
                            done2.date_submitted = todays_log.date_save
                            done2.save()

                            return redirect('IncompleteForms')
   
      
    return render (request, "Daily/formM.html", {
        'now': todays_log, 'form': form, 'selector': selector, 'profile': profile, 'read': form2
    })

def formN(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    today = datetime.date.today()
    month_name = calendar.month_name[today.month]
    form_pull = formM_model.objects.all()
    
    paved_loc = []
    for x in form_pull:
        if x.paved:
            if x.date.month == today.month:
                paved_loc.append((x.paved, x.date))  
    
    
    
    return render (request, "Monthly/formn.html", {
        'now': todays_log, 'selector': selector, 'profile': profile, 'month_name': month_name, 'paved_loc': paved_loc
    })
def formO(request, selector, weekend_day):
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    profile = user_profile_model.objects.all()
    today = datetime.date.today()
    full_name = request.user.get_full_name()
    
    month_name = calendar.month_name[today.month]

    org = formO_model.objects.all().order_by('-date')
    
    if weekend_day == 'saturday':
        ss_filler = 5
    elif weekend_day == 'sunday':
        ss_filler = 6
    
    print(ss_filler)
    if formO_model.objects.count() != 0:
        database_form = org[0]
        database_date = database_form.date
    else:
        database_date = ''
        
        
    if selector != 'form':
        for x in org:
            if str(x.date) == str(selector):
                database_model = x
        data_form = database_model
      
    else:           
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                if todays_log.date_save == database_date: 
                    initial_data = {
                        'observer' : database_form.observer,
                        'month' : database_form.month,
                        'date' : database_form.date,
                        'weekend_day' : database_form.weekend_day,
                        'Q_1' : database_form.Q_1,
                        'Q_2' : database_form.Q_2,
                        'Q_3' : database_form.Q_3,
                        'Q_4' : database_form.Q_4,
                        'Q_5' : database_form.Q_5,
                        'Q_6' : database_form.Q_6,
                        'Q_7' : database_form.Q_7,
                        'Q_8' : database_form.Q_8,
                        'Q_9' : database_form.Q_9,
                        'comments' : database_form.comments,
                        'actions_taken' : database_form.actions_taken,
                    }
                    data_form = formO_form(initial = initial_data)

                    if request.method == 'POST':
                        data_form = formO_form(request.POST, instance= database_form)
                        if data_form.is_valid():
                            A = data_form.save()

                            if 'Yes' in {
                                A.Q_2,
                                A.Q_3,
                                A.Q_4,
                                A.Q_5,
                                A.Q_6,
                                A.Q_7,
                                A.Q_8,
                                A.Q_9,
                            }:
                                issue_page = '../../../issues_view/O/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)

                            done = Forms.objects.filter(form='O')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else: 
                    initial_data = {
                        'date' : today,
                        'observer' : full_name,
                        'month' : month_name,
                        'weekend_day' : ss_filler,
                    }
                    data_form = formO_form(initial = initial_data)

                    if request.method == 'POST':
                        data_form = formO_form(request.POST)
                        if data_form.is_valid():
                            A = data_form.save()

                            if 'Yes' in {
                                A.Q_2,
                                A.Q_3,
                                A.Q_4,
                                A.Q_5,
                                A.Q_6,
                                A.Q_7,
                                A.Q_8,
                                A.Q_9,
                            }:
                                issue_page = '../../../issues_view/P/' + str(todays_log.date_save) + '/form'

                                return redirect (issue_page)
                        
                            done = Forms.objects.filter(form='O')[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                batt_prof = '../../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        else:
            batt_prof = '../../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)
    
    return render (request, "Weekly/formO.html", {
        'selector': selector, 'profile': profile, 'data_form': data_form, 'weekend_day': weekend_day
    })
def formP(request, selector, weekend_day):
    profile = user_profile_model.objects.all()
    today = datetime.date.today()
    full_name = request.user.get_full_name()
    
    month_name = calendar.month_name[today.month]

    org = formP_model.objects.all().order_by('-date')
    
    if weekend_day == 'saturday':
        ss_filler = 5
    elif weekend_day == 'sunday':
        ss_filler = 6
    
    if formP_model.objects.count() != 0:
        database_form = org[0]
        database_date = database_form.date
    else:
        database_date = ''
    
    if now.month == todays_log.date_save.month:
        if now.day == todays_log.date_save.day:
            if todays_log.date_save == database_date: 
                initial_data = {
                    'observer' : database_form.observer,
                    'month' : database_form.month,
                    'date' : database_form.date,
                    'weekend_day' : database_form.weekend_day,
                    'Q_1' : database_form.Q_1,
                    'Q_2' : database_form.Q_2,
                    'Q_3' : database_form.Q_3,
                    'Q_4' : database_form.Q_4,
                    'Q_5' : database_form.Q_5,
                    'Q_6' : database_form.Q_6,
                    'Q_7' : database_form.Q_7,
                    'Q_8' : database_form.Q_8,
                    'Q_9' : database_form.Q_9,
                    'comments' : database_form.comments,
                    'actions_taken' : database_form.actions_taken,
                }
                data_form = formO_form(initial = initial_data)

                if request.method == 'POST':
                    data_form = formO_form(request.POST, instance= database_form)
                    if data_form.is_valid():
                        A = data_form.save()
                        
                        if 'Yes' in {
                            A.Q_2,
                            A.Q_3,
                            A.Q_4,
                            A.Q_5,
                            A.Q_6,
                            A.Q_7,
                            A.Q_8,
                            A.Q_9,
                        }:
                            issue_page = '../../../issues_view/P/' + str(todays_log.date_save) + '/form'

                            return redirect (issue_page)
                        
                        done = Forms.objects.filter(form='P')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()
                        
                        return redirect('IncompleteForms')
            else: 
                initial_data = {
                    'date' : today,
                    'observer' : full_name,
                    'month' : month_name,
                    'weekend_day' : ss_filler,
                }
                data_form = formP_form(initial = initial_data)

                if request.method == 'POST':
                    data_form = formP_form(request.POST)
                    if data_form.is_valid():
                        A = data_form.save()
                        
                        if 'Yes' in {
                            A.Q_2,
                            A.Q_3,
                            A.Q_4,
                            A.Q_5,
                            A.Q_6,
                            A.Q_7,
                            A.Q_8,
                            A.Q_9,
                        }:
                            issue_page = '../../../issues_view/P/' + str(todays_log.date_save) + '/form'

                            return redirect (issue_page)
                        
                        done = Forms.objects.filter(form='P')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()
                        
                        return redirect('IncompleteForms')
        else:
            batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

            return redirect(batt_prof)
    else:
        batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)
    
    return render (request, "Weekly/formP.html", {
        'selector': selector, 'profile': profile, 'data_form': data_form, 'weekend_day': weekend_day
    })
def spill_kits(request, access_page):
    sk_form = spill_kits_form
    
    
    return render(request, 'Monthly/spillkits.html', {
        'sk_form':sk_form,
    })
def issues_view(request, form_name, form_date, access_page):
    unlock = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock == True
    
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    if access_page == 'form':
        data = Forms.objects.all()
        today = datetime.date.today()
        if today.weekday() == 5:
            day = 'saturday'
        elif today.weekday() == 6:
            day = 'sunday'
            
        for x in data:
            if x.form == form_name:
                if x.form in {'O','P'}:
                    link = x.frequency + '/' + x.link + '/' + access_page + '/' + day
                else:
                    link = x.frequency + '/' + x.link + '/' + access_page
    
    if access_page == 'issue':
        org = issues_model.objects.all().order_by('-date')
        database_form = org[0]
        
        for entry in org:
            if str(form_date) == str(entry.date):
                if form_name == entry.form:
                    picker = entry
                    form = issues_form()
                    link = ''

    elif access_page == 'edit':
        org = issues_model.objects.all().order_by('-date')
        database_form = org[0]
        
        for entry in org:
            if str(form_date) == str(entry.date):
                if form_name == entry.form:
                    picker = entry
                    link = ''
                    
        initial_data = {
            'form' : picker.form,
            'issues' : picker.issues,
            'notified' : picker.notified,
            'time' : picker.time,
            'date' : picker.date,
            'cor_action' : picker.cor_action
        }

        form = issues_form(initial=initial_data)

        if request.method == "POST":
            data = issues_form(request.POST, instance= picker)
            if data.is_valid():
                data.save()

                return redirect('../../../issues_view/' + form_name + '/' + form_date + '/issue')
    else:
        picker = 'n/a'
        if issues_model.objects.count() != 0:
            org = issues_model.objects.all().order_by('-date')
            database_form = org[0]
            
            if todays_log.date_save == database_form.date:
                if database_form.form == form_name:
                    initial_data = {
                        'form' : database_form.form,
                        'issues' : database_form.issues,
                        'notified' : database_form.notified,
                        'time' : database_form.time,
                        'date' : database_form.date,
                        'cor_action' : database_form.cor_action
                    }

                    form = issues_form(initial=initial_data)

                    if request.method == "POST":
                        data = issues_form(request.POST, instance= database_form)
                        if data.is_valid():
                            data.save()

                            done = Forms.objects.filter(form=form_name)[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'date' : todays_log.date_save,
                        'form' : form_name
                    }
                    form = issues_form(initial=initial_data)

                    if request.method == "POST":
                        data = issues_form(request.POST)
                        if data.is_valid():
                            data.save()

                            done = Forms.objects.filter(form=form_name)[0]
                            done.submitted = True
                            done.date_submitted = todays_log.date_save
                            done.save()

                            return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date' : todays_log.date_save,
                    'form' : form_name
                }
                form = issues_form(initial=initial_data)

                if request.method == "POST":
                    data = issues_form(request.POST)
                    if data.is_valid():
                        data.save()

                        done = Forms.objects.filter(form=form_name)[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
        else:
            initial_data = {
                'date' : todays_log.date_save,
                'form' : form_name
            }
            form = issues_form(initial=initial_data)

            if request.method == "POST":
                data = issues_form(request.POST)
                if data.is_valid():
                    data.save()

                    done = Forms.objects.filter(form=form_name)[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')
            
    return render (request, "ees_forms/issues_template.html", {
        'form': form, 'access_page': access_page, 'picker': picker, 'form_name': form_name, "form_date": form_date, 'link':link, 'profile': profile, "unlock": unlock
    })

def corrective_action_view(request):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
        
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    
    ca_forms = issues_model.objects.all().order_by('-id')
    
    return render (request, "ees_forms/corrective_actions.html", {
        'ca_forms': ca_forms, 'profile': profile, 'client': client, ##'submitted': submitted, "back": back
    })

def calendar_view(request, year, month):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    
    profile = user_profile_model.objects.all()
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    prev_month_num = month_number - 1
    next_month_num = month_number + 1
    
    
    if month_number == 1:
        prev_month = str(calendar.month_name[12])
        prev_year = str(year - 1)
    else:
        prev_month = str(calendar.month_name[month_number - 1])
        prev_year = year
    
    if month_number == 12:
        next_month = str(calendar.month_name[1])
        next_year = str(year + 1)
    else:
        next_month = str(calendar.month_name[month_number + 1])
        next_year = year
        
    events = Event.objects.all()
    
    
 
    calend = Calendar()
    calend.setfirstweekday(6)
    html_cal = calend.formatmonth(year, month_number, year, withyear=True)
    
    
    
    return render (request, "ees_forms/schedule.html", {
        'year': year, 'month': month, 'prev_month': prev_month, 'next_month': next_month, 'events': events, 'html_cal': html_cal, 'prev_year': prev_year, 'next_year': next_year, 'profile': profile, 'unlock': unlock, 'client':client,
    })


def schedule_view(request):
    today_year = int(datetime.date.today().year)
    today_month = str(calendar.month_name[datetime.date.today().month])
    
    return redirect ('schedule/' + str(today_year) + '/' + str(today_month))
    
    return render (request, "ees_forms/scheduling.html", {
        'today_year': today_year, 'today_month': today_month, #'prev_month': prev_month, 'cal': cal, 'next_month': next_month,
    })

def event_add_view(request):
    profile = user_profile_model.objects.all()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    
    form_var = events_form()
       
    if request.method == "POST":
        request_form = events_form(request.POST)
        if request_form.is_valid():
            request_form.save()

            cal_link = 'schedule/' + str(today_year) + '/' + today_month

            return redirect(cal_link)
    
    
    return render (request, "ees_forms/event_add.html", {
        'today_year': today_year, 'today_month': today_month, 'form': form_var, 'profile': profile,
    })

def event_detail_view(request, access_page, event_id):
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    
    form = events_form()
    if access_page == 'view':
        my_event = Event.objects.get(pk=event_id)
    elif access_page == 'edit':
        data_pull = Event.objects.get(pk=event_id)
        initial_data = {
            'observer' : data_pull.observer,
            'title' : data_pull.title,
            'date' : data_pull.date,
            'start_time' : data_pull.start_time,
            'end_time' : data_pull.end_time,
            'notes' : data_pull.notes,
        }
        my_event = events_form(initial=initial_data)
        
        if request.method == 'POST':
            data = events_form(request.POST, instance= data_pull)
            print('pork')
            if data.is_valid():
                print('chicken')
                data.save()
                
                return redirect ('../../event_detail/' + str(event_id) + '/view')
    
    return render (request, "ees_forms/event_detail.html", {
        'today_year': today_year, 'today_month': today_month, 'form': form, 'my_event': my_event, 'event_id': event_id, 'access_page': access_page
    })

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name='ees_forms/ees_password.html'
    
    def get_success_url(self):
        return reverse('profile', kwargs={'access_page': 'success'})
    
    #success_url = reverse_lazy('profile')
    

















def profile_redirect(request):
    return redirect ('profile/main')
    
    return render(request, 'profile.hmtl', {
        
    })
def about_view(request):
    profile = user_profile_model.objects.all()
    
    return render(request, 'ees_forms/ees_about.html', {
        'profile':profile,
    })
def safety_view(request):
    profile = user_profile_model.objects.all()
    
    return render(request, 'ees_forms/ees_safety.html', {
        'profile':profile,
    })
def archive_view(request):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
    profile = user_profile_model.objects.all()
    
    return render(request, 'ees_forms/ees_archive.html', {
        'profile':profile, 'client': client
    })
def search_forms_view(request, access_page):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
        
    profile = user_profile_model.objects.all()
    if access_page != 'search':
        Model = apps.get_model('EES_Forms', access_page)
        ModelForms = Forms.objects.all()
        chk_database = Model.objects.count()
        weekend = False
        
        if chk_database == 0:
            att_check = 5
        else:
            try:
                database = Model.objects.all().order_by('-date')
                for x in ModelForms:
                    f = access_page[4] + '-' + access_page[5]

                    if x.form == access_page[4]:
                        if x.frequency[0] == 'W':
                            att_check = 4
                            if x.weekend_only:
                                weekend = True
                            else:
                                weekend = False
                        else:
                            att_check = 1
                            print('no')
                    elif x.form == access_page[4] + '-' + access_page[5]:
                        if x.frequency[0] == 'W':
                            att_check = 4
                        else:
                            att_check = 1
                    else:
                        print('Error - EES_00005')
            except FieldError as e:
                database = Model.objects.all().order_by('-week_start')
                for x in ModelForms:
                    if x.form == access_page[4]:
                        if x.frequency[0] == 'D':
                            att_check = 3
                        else:
                            att_check = 2
                    elif x.form == access_page[4] + '-' + access_page[5]:
                        if x.frequency[0] == 'D':
                            att_check = 3
                        else:
                            att_check = 2
                    print('Error - EES_00006')
    if request.method == "POST":
        searched = request.POST['searched']
        database = ''
        att_check = ''
        weekend = False
        
        
        form_list = Forms.objects.filter(Q(form__icontains= searched) | Q(frequency__icontains= searched) | Q(title__icontains= searched))
        
        forms_pre = Forms.objects.filter(form__contains= searched)
        forms = form_list.order_by('form')
        
        
        
        
        return render(request, 'ees_forms/search_forms.html', {
        'profile':profile, 'searched':searched, 'forms':forms, 'access_page': access_page, 'database': database, 'att_check':att_check, 'weekend': weekend,  'client': client,
        })
    else:
        return render(request, 'ees_forms/search_forms.html', {
        'profile':profile,'access_page': access_page, 'database': database, 'att_check':att_check, 'weekend': weekend, 'client': client,
        })
    
    
def c_dashboard_view(request):
    if request.user.groups.filter(name='EES Coke Employees') or request.user.is_superuser or request.user.groups.filter(name='SGI Admin'):
        client = False
        if request.user.groups.filter(name='EES Coke Employees'):
            client = True
            
            
        today = datetime.date.today()
        profile = user_profile_model.objects.all()
        daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
        todays_log = daily_prof[0]
    
    #----USER ON SCHEDULE----------

        event_cal = Event.objects.all()
        today = datetime.date.today()

        for x in event_cal:
            if x.date == today:
                todays_obser = x.observer
    #---90 DAY PUSH-------

        reads = formA5_readings_model.objects.all()
        data = formA5_model.objects.all()

        def all_ovens(reads):
            A = []
            for items in reads:
                date = items.form.date
              #  date_array = date.split("-")

                year = date.year
                month = date.month
                day = date.day

                form_date = datetime.datetime(year, month, day)
                added_date = form_date + datetime.timedelta(days=91)
                due_date = added_date - datetime.datetime.now() 

                if len(str(items.o1)) == 1 :
                    oven1 = "0" + str(items.o1)
                else:
                    oven1 = items.o1
                A.append((oven1, items.form.date, added_date.date, due_date.days)) 

                if len(str(items.o2)) == 1 :
                    oven2 = "0" + str(items.o2)
                else:
                    oven2 = items.o2
                A.append((oven2, items.form.date, added_date.date, due_date.days))

                if len(str(items.o3)) == 1 :
                    oven3 = "0" + str(items.o3)
                else:
                    oven3 = items.o3
                A.append((oven3, items.form.date, added_date.date, due_date.days))    

                if len(str(items.o4)) == 1 :
                    oven4 = "0" + str(items.o4)
                else:
                    oven4 = items.o4
                A.append((oven4, items.form.date, added_date.date, due_date.days))      

            return A   

        hello = all_ovens(reads)
        func = lambda x: (x[0], x[1])
        sort = sorted(hello, key = func, reverse=True)
       # print (sort)

        def final(sort):
            B = []
            i = 1
            for new in sort:
                B.append(new)

            for x in sort:
                for y in range(i, len(sort)):
                    tree = sort[y]
                    if tree[0] == x[0]:
                        if tree in B:
                            B.remove(tree)
                i+=1
            return B
        cool = final(sort)

        def overdue_30(cool):
            C = []
            for x in cool:
                if x[3] <= 30 :
                    C.append(x)
            return C

        def overdue_10(cool):
            D = []
            for x in cool:
                if x[3] <= 10 :
                    D.append(x)
            return D

        def overdue_5(cool):
            E = []
            for x in cool:
                if x[3] <= 5 :
                    E.append(x)
            return E

        def overdue_closest(cool):
            F = []

            func2 = lambda R: (R[3])  
            sort2 = sorted(cool, key = func2)
            most_recent = sort2[0][3]

            for x in sort2:
                if x[3] == most_recent:
                    F.append(x)
            return F

        od_30 = overdue_30(cool)
        od_10 = overdue_10(cool)
        od_5 = overdue_5(cool)
        od_recent = overdue_closest(cool)
    #----WEATHER TAB-----------
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'

        city = 'Dearborn'

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'wind_speed' : city_weather['wind']['speed'],
            'wind_direction' : city_weather['wind']['deg'],
            'humidity' : city_weather['main']['humidity'],
        }

        degree = weather['wind_direction']


        def toTextualDescription(degree):
            if degree > 337.5:
                return 'N'
            if degree > 292.5:
                return 'NW'
            if degree > 247.5:
                return 'W'
            if degree > 202.5:
                return 'SW'
            if degree > 157.5:
                return 'S'
            if degree > 122.5:
                return 'SE'
            if degree > 67.5:
                return 'E'
            if degree > 22.5:
                return 'NE'
            return 'N'

        wind_direction = toTextualDescription(degree)
        
    #----ISSUES/CORRECTIVE ACTIONS----------  
        
        ca_forms = issues_model.objects.all().order_by('-id')
        
    #------------USERS-------------------
    
        Users = User.objects.all()
        profile = user_profile_model.objects.all()
        
    #------FORM A-1 COLLECTION MAIN PRESURES---------
    
        formA1 = formA1_readings_model.objects.all().order_by('-form')
        recent_A1 = formA1[0]
        if str(today) == str(recent_A1):
            none_A1 = False
            charges = [('Charge #1', str(recent_A1.c1_sec) + ' sec'), ('Charge #2', str(recent_A1.c2_sec) + ' sec'), ('Charge #3', str(recent_A1.c3_sec) + ' sec'), ('Charge #4', str(recent_A1.c4_sec) + ' sec'), ('Charge #5', str(recent_A1.c5_sec) + ' sec'), ('Total Seconds', str(recent_A1.total_seconds) + ' sec')]
        else:
            none_A1 = True
            charges = [('Charge #1', 'N/A'), ('Charge #2', 'N/A'), ('Charge #3', 'N/A'), ('Charge #4', 'N/A'), ('Charge #5', 'N/A'), ('Total Seconds', 'N/A')]
            
    #------FORM A-4 COLLECTION MAIN PRESURES---------
    
        formA4 = formA4_model.objects.all().order_by('-date')
        recent_A4 = formA4[0]
        if str(today) == str(recent_A4):
            none_A4 = False
            pressures = [('Main #1', recent_A4.main_1), ('Main #2', recent_A4.main_2), ('Main #3', recent_A4.main_3), ('Main #4', recent_A4.main_4), ('Suction Main', recent_A4.suction_main)]
        else:
            none_A4 = True
            pressures = [('Main #1', 'N/A'), ('Main #2', 'N/A'), ('Main #3', 'N/A'), ('Main #4', 'N/A'), ('Suction Main', 'N/A')]
            
    #-----PUSH TRAVELS--------------
    
        if len(str(today.month)) == 1:
            month = '0' + str(today.month)
        else:
            month = str(today.month)
            
        if len(str(today.day)) == 1:
            day = '0' + str(today.day)
        else:
            day = str(today.day)
            
        date_trans = str(today.year) + '-' + month + '-' + day
    
        org = formA5_model.objects.all().order_by('-date')
        database_form = org[0]
        org2 = formA5_readings_model.objects.all().order_by('-form')
        reads = org2[0]
        
        def double_digit(x):
            if len(x) == 1:
                double = '0' + x
                return double
            else:
                return x
             
        if str(todays_log.date_save) == str(database_form.date):
            ovens_reads = [
                {(reads.o1, 'p') : (
                    double_digit(reads.o1_1_reads), 
                    double_digit(reads.o1_2_reads), 
                    double_digit(reads.o1_3_reads), 
                    double_digit(reads.o1_4_reads), 
                    double_digit(reads.o1_5_reads), 
                    double_digit(reads.o1_6_reads), 
                    double_digit(reads.o1_7_reads), 
                    double_digit(reads.o1_8_reads)
                ),
                 (reads.o1, 't') : (
                     double_digit(reads.o1_9_reads), 
                     double_digit(reads.o1_10_reads), 
                     double_digit(reads.o1_11_reads), 
                     double_digit(reads.o1_12_reads), 
                     double_digit(reads.o1_13_reads), 
                     double_digit(reads.o1_14_reads), 
                     double_digit(reads.o1_15_reads), 
                     double_digit(reads.o1_16_reads)
                 )
                },
                {(reads.o2, 'p') : (
                    double_digit(reads.o2_1_reads), 
                    double_digit(reads.o2_2_reads), 
                    double_digit(reads.o2_3_reads), 
                    double_digit(reads.o2_4_reads), 
                    double_digit(reads.o2_5_reads), 
                    double_digit(reads.o2_6_reads), 
                    double_digit(reads.o2_7_reads), 
                    double_digit(reads.o2_8_reads)),
                 (reads.o2, 't') : (
                     double_digit(reads.o2_9_reads), 
                     double_digit(reads.o2_10_reads), 
                     double_digit(reads.o2_11_reads), 
                     double_digit(reads.o2_12_reads), 
                     double_digit(reads.o2_13_reads), 
                     double_digit(reads.o2_14_reads), 
                     double_digit(reads.o2_15_reads), 
                     double_digit(reads.o2_16_reads))
                },
                {(reads.o3, 'p') : (
                    double_digit(reads.o3_1_reads), 
                    double_digit(reads.o3_2_reads), 
                    double_digit(reads.o3_3_reads), 
                    double_digit(reads.o3_4_reads), 
                    double_digit(reads.o3_5_reads), 
                    double_digit(reads.o3_6_reads), 
                    double_digit(reads.o3_7_reads), 
                    double_digit(reads.o3_8_reads)),
                 (reads.o3, 't') : (
                     double_digit(reads.o3_9_reads), 
                     double_digit(reads.o3_10_reads), 
                     double_digit(reads.o3_11_reads), 
                     double_digit(reads.o3_12_reads), 
                     double_digit(reads.o3_13_reads), 
                     double_digit(reads.o3_14_reads), 
                     double_digit(reads.o3_15_reads), 
                     double_digit(reads.o3_16_reads))
                },
                {(reads.o4, 'p') : (
                    double_digit(reads.o4_1_reads), 
                    double_digit(reads.o4_2_reads), 
                    double_digit(reads.o4_3_reads), 
                    double_digit(reads.o4_4_reads), 
                    double_digit(reads.o4_5_reads), 
                    double_digit(reads.o4_6_reads), 
                    double_digit(reads.o4_7_reads), 
                    double_digit(reads.o4_8_reads)),
                 (reads.o4, 't') : (
                     double_digit(reads.o4_9_reads), 
                     double_digit(reads.o4_10_reads), 
                     double_digit(reads.o4_11_reads), 
                     double_digit(reads.o4_12_reads), 
                     double_digit(reads.o4_13_reads), 
                     double_digit(reads.o4_14_reads), 
                     double_digit(reads.o4_15_reads), 
                     double_digit(reads.o4_16_reads))
                },
            ]
            highest_p_list = [
                {'o1' : max(ovens_reads[0][reads.o1, 'p'])},
                {'o2' : max(ovens_reads[1][reads.o2, 'p'])},
                {'o3' : max(ovens_reads[2][reads.o3, 'p'])},
                {'o4' : max(ovens_reads[3][reads.o4, 'p'])},
            ]
            
            highest_t_list = [
                {'o1' : max(ovens_reads[0][reads.o1, 't'])},
                {'o2' : max(ovens_reads[1][reads.o2, 't'])},
                {'o3' : max(ovens_reads[2][reads.o3, 't'])},
                {'o4' : max(ovens_reads[3][reads.o4, 't'])},
            ]
 
            highest_push = highest_p_list[0]['o1']
            highest_travel = highest_t_list[0]['o1']
            
            high_push = highest_push + "%"
            high_travel = highest_travel + '%'
            
            none_A5 = False
        else: 
            none_A5 = True
            high_push = 'N/A'
            high_travel = 'N/A'
            
        
    
            
            
    else:
        return redirect('IncompleteForms')
    
    return render(request, 'ees_forms/c_dashboard.html',{
        'profile':profile, 'high_push': high_push, 'high_travel': high_travel, 'todays_log':todays_log, 'todays_obser':todays_obser, 'od_30':od_30, 'weather': weather, "today":date_trans, 'ca_forms': ca_forms, 'wind_direction': wind_direction, 'Users': Users, 'client': client, 'pressures':pressures, 'charges':charges, 'none_A1':none_A1, "none_A4":none_A1, 'none_A5':none_A5
    })
    
    


def testView(request):
    return render(request, "ees_forms/testFile.html")

















