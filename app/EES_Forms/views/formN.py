from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formM_model
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import setUnlockClientSupervisor

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formN(request, facility, fsID, selector):
    formName = "23"
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    search = False
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    now = datetime.datetime.now().date()
    today = datetime.date.today()
    month_name = calendar.month_name[today.month]
    form_pull = formM_model.objects.filter(date__month=today.month, facilityChoice__facility_name=facility)

    if selector != 'form':
        form_pull = formM_model.objects.filter(date__month=selector[0], facilityChoice__facility_name=facility)
        month_name = calendar.month_name[int(selector[0])]
    
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

    if daily_prof.exists():
        todays_log = daily_prof[0]
    else:
        todays_log = ''

    return render(request, "shared/forms/monthly/formN.html", {
        'fsID': fsID, 'formName': formName, "client": client, 'unlock': unlock, 'supervisor': supervisor, 'search': search, 'facility': facility, 'now': todays_log, 'selector': selector, 'profile': profile, 'month_name': month_name, 'paved_loc': paved_loc, 'unpaved_loc': unpaved_loc, 'parking_loc': parking_loc,
    })
