from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form20_model
from ..forms import form20_form
from ..utils.main_utils import get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
from datetime import timedelta

lock = login_required(login_url='Login')

@lock
def form20(request, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, selector)
    facility = form_variables['facilityName']
    starting_monday = form_variables['now'] - timedelta(days=form_variables['now'].weekday())
    end_week = starting_monday + timedelta(days=4)
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if request.user.user_profile.position == "observer": 
        if form_variables['daily_prof'].exists():
            todays_log = form_variables['daily_prof'][0]
        else:
            batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    else:
        todays_log = ""
    # -----SET DECIDING VARIABLES------------
    more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID) 
    if isinstance(more_form_variables, HttpResponseRedirect):
        return more_form_variables
    else:
        data, existing, search, database_form = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID)
    # -----SET RESPONSES TO DECIDING VARIABLES------------    
    if search:
        database_form = ''
    else:
        if existing:
            print('Check 2.1')
            initial_data = get_initial_data(form20_model, database_form)
        else:
            initial_data = {
                'week_start': starting_monday,
                'week_end': end_week
            }
        data = form20_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
    if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
        try:
            form_settings = form_variables['freq']
        except form_settings_model.DoesNotExist:
            raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
        if existing:
            form = form20_form(request.POST, instance=database_form, form_settings=form_settings)
        else:
            form = form20_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
        exportVariables = (request, selector, facility, database_form, fsID)
        return redirect(*template_validate_save(form, form_variables, *exportVariables))
    return render(request, "shared/forms/daily/form20.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        "search": search, 
        'supervisor': form_variables['supervisor'], 
        'todays_log': todays_log, 
        'empty': data, 
        'selector': selector, 
        'formName': form_variables['formName'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
    })
