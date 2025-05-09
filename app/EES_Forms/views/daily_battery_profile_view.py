from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import daily_battery_profile_model, user_profile_model, facility_model
from ..forms import daily_battery_profile_form
from django.conf import settings # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils.main_utils import setUnlockClientSupervisor, getCompanyFacilities
import re

lock = login_required(login_url='Login')

@lock
def daily_battery_profile_view(request, facility, access_page, date):
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = user_profile_model.objects.all()
    now = datetime.datetime.now().date()
    form = daily_battery_profile_form
    options = facility_model.objects.filter(facility_name=facility)[0]
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    existing = False
    todays_log = ''

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if now == todays_log.date_save:
            existing = True
    
    if existing:
        if todays_log.inop_numbs == "-":
            inop_numbers = todays_log.inop_numbs
        else:
            inop_numbers = todays_log.inop_numbs[1:-1].replace("'", "")
        initial_data = {
            'facilityChoice': todays_log.facilityChoice,
            'foreman': todays_log.foreman,
            'crew': todays_log.crew,
            'inop_ovens': todays_log.inop_ovens,
            'inop_numbs': inop_numbers,
            'date_save': todays_log.date_save,
        }
    else:
        initial_data = {
            'facilityChoice': options
        }

    form = daily_battery_profile_form(initial=initial_data)
    if request.method == 'POST':
        print(request.POST)
        if existing:
            form = daily_battery_profile_form(request.POST, instance=todays_log)
        else:
            form = daily_battery_profile_form(request.POST)
        
        if form.is_valid():
            A = form.save(commit=False)
            A.facilityChoice = options
            if A.inop_numbs in ['-', 'None']:
                A.inop_ovens = 0
                A.inop_numbs = []
            else:
                A.inop_ovens = len(request.POST['inop_numbs'].replace(' ', ''). split(','))
                
                newList = []
                for x in request.POST['inop_numbs'].split(','):
                    x = int(re.sub("[^0-9]", "", x))
                    newList.append(x)
                A.inop_numbs = newList
            A.save()
            return redirect('IncompleteForms', facility)

    return render(request, "observer/Bat_Info.html", {
        'supervisor': supervisor, "client": client, 'unlock': unlock, 'form': form, 'todays_log': todays_log, 'profile': profile, 'access_page': access_page, 'facility': facility
    })

@lock
def facility_select_view(request, facility):
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profileFacs = getCompanyFacilities(request.user.user_profile.company.company_name)
    profile = user_profile_model.objects.all()
    loginPage = True
    now = datetime.datetime.now().date()
    if request.method == 'POST':
        answer = request.POST['facility']
        daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=answer).order_by('-date_save')
        if answer != '':
            print('CHECK 01')
            batteryQuery = facility_model.objects.get(facility_name=answer)
            print(batteryQuery)
            print(batteryQuery.is_battery)
            print(batteryQuery.dashboard)
            if batteryQuery.is_battery == 'Yes' and batteryQuery.dashboard == 'battery':
                print('CHECK 02')
                if daily_prof.exists():
                    todays_log = daily_prof[0]
                    if now == todays_log.date_save:
                        return redirect('IncompleteForms', answer)
                batt_prof = '../../' + answer + '/daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
                return redirect(batt_prof)
            elif batteryQuery.dashboard == "default":
                print('CHECK 03')
                return redirect('defaultDash', answer)

    return render(request, "observer/facility_select.html", {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'options': profileFacs, 
        'loginPage': loginPage, 
        'profile': profile, 
        'facility': facility
    })
