from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form6_model
from ..forms import form6_form
from ..utils import weatherDict, get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json
from datetime import timedelta

lock = login_required(login_url='Login')

@lock
def form6(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    last_monday = form_variables['now'] - timedelta(days=form_variables['now'].weekday())
    one_week = timedelta(days=4)
    end_week = last_monday + one_week
    freq2 = False
    fridayDate = form_variables['now'] + timedelta(days=(4 - form_variables['now'].weekday()))
    if 2 < form_variables['now'].month < 11:
        freq2 = True
    elif form_variables['now'].month == 2 and fridayDate.month == (form_variables['now'].month + 1):
        freq2 = True
    elif form_variables['now'].month == 10 and fridayDate.month == (form_variables['now'].month + 1):
        freq2 = True

    # Weather API Pull
    weather = weatherDict(form_variables['freq'].facilityChoice.city)
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
    # -----SET DECIDING VARIABLES------------
        more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request) 
        if isinstance(more_form_variables, HttpResponseRedirect):
            return more_form_variables
        else:
            data, existing, search, database_form = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request)
    # -----SET RESPONSES TO DECIDING VARIABLES------------
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = get_initial_data(form6_model, database_form)
            else:
                initial_data = {
                    'week_start': last_monday,
                    'week_end': end_week,
                }
            data = form6_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form6_form(request.POST, instance=database_form, form_settings=form_settings)
            else:
                form = form6_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/form6.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        'weather': json.dumps(weather), 
        "search": search, 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
         
        'todays_log': todays_log, 
        'end_week': end_week, 
        'data': data,
        'selector': selector, 
        'formName': form_variables['formName'], 
        'notifs': form_variables['notifs'],
        'freq2': freq2,
        'freq': form_variables['freq'],
        'facility': facility
    })
