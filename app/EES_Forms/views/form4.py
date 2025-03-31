from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form4_model
from ..forms import form4_form
from ..utils import get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json

lock = login_required(login_url='Login')

@lock
def form4(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
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
            leaks = ''
            collect_Raw_JSON = json.loads(data.leak_data)
            if len(collect_Raw_JSON) > 0:
                collect_json = collect_Raw_JSON['data']
            else:
                collect_json = ''
            
            if data.leak_data == '{}':
                leaks = 'no'
            elif data.leak_data == '':
                leaks = 'no data'
            else:
                leaks = 'yes'
        else:
            if existing:
                initial_data = get_initial_data(form4_model, database_form)
                if initial_data['leak_data'] == '{}':
                    leaks = 'no'
                else:
                    leaks = 'yes'
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': form_variables['full_name'],
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'facility_name': facility,
                }
                leaks = 'no data'

            data = form4_form(initial=initial_data, form_settings=form_variables['freq'])
            collect_json = ''
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS------------
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form4_form(request.POST, instance=database_form, form_settings=form_settings)
            else:
                form = form4_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))        
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    return render(request, "shared/forms/daily/form4.html", {
        'picker': form_variables['picker'], 
        'leaks': leaks,
        'collect_json': collect_json, 
        'options': form_variables['freq'].facilityChoice, 
        "search": search, 
        'existing': existing, 
        "client": form_variables['client'], 
        "supervisor": form_variables['supervisor'], 
         
        'todays_log': todays_log, 
        'data': data, 
        'formName': form_variables['formName'], 
        'selector': selector, 
        'unlock': form_variables['unlock'], 
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'fsID': fsID
    })
