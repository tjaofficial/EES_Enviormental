from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import daily_battery_profile_model, user_profile_model, bat_info_model
from ..forms import daily_battery_profile_form
from django.conf import settings
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from .supervisor_view import getCompanyFacilities
from ..utils import setUnlockClientSupervisor
import re

lock = login_required(login_url='Login')

@lock
def daily_battery_profile_view(request, facility, access_page, date):
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    profile = user_profile_model.objects.all()
    now = datetime.datetime.now().date()
    form = daily_battery_profile_form
    options = bat_info_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    existing = False
    todays_log = ''

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if now == todays_log.date_save:
            existing = True
    
    if existing:
        initial_data = {
            'facilityChoice': todays_log.facilityChoice,
            'foreman': todays_log.foreman,
            'crew': todays_log.crew,
            'inop_ovens': todays_log.inop_ovens,
            'inop_numbs': todays_log.inop_numbs,
            'date_save': todays_log.date_save,
        }
    else:
        initial_data = {
            'facilityChoice': options.filter(facility_name=facility)[0]
        }

    form = daily_battery_profile_form(initial=initial_data)
    if request.method == 'POST':
        if existing:
            form = daily_battery_profile_form(request.POST, instance=todays_log)
        else:
            form = daily_battery_profile_form(request.POST)
        
        if form.is_valid():
            A = form.save(commit=False)
            if A.inop_numbs == '-':
                A.inop_ovens = 0
            else:
                A.inop_ovens = len(request.POST['inop_numbs'].replace(' ', ''). split(','))
                
                newList = []
                for x in request.POST['inop_numbs'].split(','):
                    x = re.sub("[^0-9]", "", x)
                    newList.append(x)
                A.inop_numbs = newList
            A.save()
            return redirect('IncompleteForms', facility)

    return render(request, "ees_forms/Bat_Info.html", {
        'supervisor': supervisor, "client": client, 'unlock': unlock, 'options': options, 'form': form, 'todays_log': todays_log, 'profile': profile, 'access_page': access_page, 'facility': facility
    })

@lock
def facility_select_view(request):
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    profileFacs = getCompanyFacilities(request.user.username)
    profile = user_profile_model.objects.all()
    loginPage = True
    now = datetime.datetime.now().date()
    if request.method == 'POST':
        answer = request.POST['facility']
        daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=answer).order_by('-date_save')
        if answer != '':
            if daily_prof.exists():
                todays_log = daily_prof[0]
                if now == todays_log.date_save:
                    return redirect('IncompleteForms', answer)
            batt_prof = '../' + answer + '/daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect(batt_prof)

    return render(request, "ees_forms/facility_select.html", {
        'supervisor': supervisor, "client": client, 'unlock': unlock, 'options': profileFacs, 'loginPage': loginPage, 'profile': profile, 
    })
