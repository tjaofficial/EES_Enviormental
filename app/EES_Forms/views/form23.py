from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import user_profile_model, form22_model
from ..initial_form_variables import initiate_form_variables
from collections import defaultdict
import calendar

lock = login_required(login_url='Login')

@lock
def form23(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    grouped_data = {
        "roads": defaultdict(list),
        "paved_roads": defaultdict(list),
        "parking_lots": defaultdict(list)
    }
    grouped_data["roads"]["Main Street"].append("2025-03-01")
    print(grouped_data)
    search = False
    profile = user_profile_model.objects.all()
    form_pull = form22_model.objects.filter(date__month=form_variables['now'].month, formSettings__facilityChoice__facility_name=facility)
    month_name = calendar.month_name[form_variables['now'].month]

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

    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
    else:
        todays_log = ''

    return render(request, "shared/forms/monthly/formN.html", {
        'fsID': fsID, 
        'formName': form_variables['formName'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'search': search, 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'now': todays_log, 
        'selector': selector, 
        'profile': profile, 
        'month_name': month_name, 
        'paved_loc': paved_loc, 
        'unpaved_loc': unpaved_loc, 
        'parking_loc': parking_loc,
    })
