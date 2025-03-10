from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime, date
from ..models import Forms, user_profile_model, daily_battery_profile_model, form22_model
import calendar
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, setUnlockClientSupervisor

lock = login_required(login_url='Login')



@lock
def formN(request, facility, fsID, selector):
    formName = "23"
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    profile = user_profile_model.objects.all()
    today = date.today()
    form_pull = form22_model.objects.filter(date__month=today.month, facilityChoice__facility_name=facility)
    month_name = calendar.month_name[today.month]

    if selector != 'form':
        form_pull = form22_model.objects.filter(date__month=selector[0], facilityChoice__facility_name=facility)
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
        'fsID': fsID, 
        'formName': formName, 
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        'search': search, 
        'facility': facility, 
        'notifs': notifs,
        'freq': freq,
        'now': todays_log, 
        'selector': selector, 
        'profile': profile, 
        'month_name': month_name, 
        'paved_loc': paved_loc, 
        'unpaved_loc': unpaved_loc, 
        'parking_loc': parking_loc,
    })
