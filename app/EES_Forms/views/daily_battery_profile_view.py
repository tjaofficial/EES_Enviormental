from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import daily_battery_profile_model, user_profile_model, bat_info_model
from ..forms import daily_battery_profile_form
from django.conf import settings
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

lock = login_required(login_url='Login')


@lock
def daily_battery_profile_view(request, facility, access_page, date):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=CLIENT_VAR):
        unlock = True
    if request.user.groups.filter(name=OBSER_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
        
    profile = user_profile_model.objects.all()
    now = datetime.datetime.now()
    form = daily_battery_profile_form
    options = bat_info_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    existing = False
    todays_log = ''

    if len(daily_prof) > 0:
        todays_log = daily_prof[0]
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                if now.year == todays_log.date_save.year:
                    existing = True
    
    if existing:
        initial_data = {
            'facility': todays_log.facility,
            'foreman': todays_log.foreman,
            'crew': todays_log.crew,
            'inop_ovens': todays_log.inop_ovens,
            'inop_numbs': todays_log.inop_numbs,
            'date_save': todays_log.date_save,
        }
    else:
        initial_data = {
            'facility': facility
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
            A.save()
            return redirect('IncompleteForms', facility)

    return render(request, "ees_forms/Bat_Info.html", {
        'supervisor': supervisor, "client": client, 'unlock': unlock, 'options': options, 'form': form, 'now': now, 'todays_log': todays_log, 'profile': profile, 'access_page': access_page, 'facility': facility
    })

@lock
def facility_select_view(request):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=CLIENT_VAR):
        unlock = True
    if request.user.groups.filter(name=OBSER_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
        
    if len(user_profile_model.objects.filter(user=request.user)) > 0:
        profileComapny = user_profile_model.objects.filter(user=request.user)[0].company
        profileFacs = bat_info_model.objects.filter(company=profileComapny)

    profile = user_profile_model.objects.all()
    
    loginPage = True
    now = datetime.datetime.now()
    count_bp = daily_battery_profile_model.objects.count()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    if request.method == 'POST':
        answer = request.POST['facility']
        if answer != '':
            if count_bp != 0:
                todays_log = daily_prof[0]
                if now.month == todays_log.date_save.month:
                    if now.day == todays_log.date_save.day:
                        return redirect('IncompleteForms', answer)

            batt_prof = '../' + answer + '/daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect(batt_prof)

    return render(request, "ees_forms/facility_select.html", {
        'supervisor': supervisor, "client": client, 'unlock': unlock, 'options': profileFacs, 'now': now, 'loginPage': loginPage, 'profile': profile, 
    })
