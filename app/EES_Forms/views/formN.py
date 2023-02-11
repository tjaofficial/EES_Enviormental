from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formM_model
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formN(request, facility, selector):
    unlock = False
    client = False
    search = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    month_name = calendar.month_name[today.month]
    form_pull = formM_model.objects.all().filter(date__month=today.month)
    count_bp = daily_battery_profile_model.objects.count()
    if selector != 'form':
        form_pull = formM_model.objects.all().filter(date__month=selector)
    
    paved_loc = []
    for x in form_pull:
        if x.paved:
            paved_loc.append((x.paved, x.date))
    
    unpaved_loc = []
    for x in form_pull:
        if x.unpaved:
            unpaved_loc.append((x.unpaved, x.date))
                
    parking_loc = []
    for x in form_pull:
        if x.parking:
            parking_loc.append((x.parking, x.date))

    if count_bp != 0:
        todays_log = daily_prof[0]
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Monthly/formN.html", {
        "client": client, 'unlock': unlock, 'supervisor': supervisor, 'search': search, 'facility': facility, 'now': todays_log, 'selector': selector, 'profile': profile, 'month_name': month_name, 'paved_loc': paved_loc, 'unpaved_loc': unpaved_loc, 'parking_loc': parking_loc,
    })
