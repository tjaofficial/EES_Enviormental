from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form27_model
from ..forms import form27_form
from ..utils import what_quarter, get_initial_data, fix_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
from datetime import datetime

lock = login_required(login_url='Login')

@lock
def form27(request, facility, fsID, selector):
    fix_data(fsID)
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
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
                initial_data = get_initial_data(form27_model, database_form)
            else:
                initial_data = {
                    'quarter': what_quarter(form_variables['now']),
                    'date': form_variables['now'],
                }
            data = form27_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form27_form(request.POST, instance=database_form, form_settings=form_settings)
            else:
                form = form27_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
            
    return render(request, "shared/forms/quarterly/form27.html", {
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        "search": search, 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'formName': form_variables['formName'], 
        'selector': selector, 
        'data': data,
        'fsID': fsID,
    })