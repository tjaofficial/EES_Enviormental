from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form9_model
from ..forms import form9_form
from ..utils.main_utils import get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json

lock = login_required(login_url='Login')

@lock
def form9(request, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, selector)
    facility = form_variables['facilityName']
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
        goose_neck_data_raw_JSON = json.loads(data.goose_neck_data)
        if len(goose_neck_data_raw_JSON) > 0:
            goose_neck_data_JSON = goose_neck_data_raw_JSON['data']
        else:
            goose_neck_data_JSON = ''
    else:
        if existing:
            initial_data = get_initial_data(form9_model, database_form)
        else:
            initial_data = {
                'date': todays_log.date_save,
                'observer': form_variables['full_name'],
                'crew': todays_log.crew,
                'foreman': todays_log.foreman,
            }
        goose_neck_data_JSON = ''
        data = form9_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
    if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
        try:
            form_settings = form_variables['freq']
        except form_settings_model.DoesNotExist:
            raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
        if existing:
            data = form9_form(request.POST, instance=database_form, form_settings=form_settings)
        else:
            data = form9_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
        exportVariables = (request, selector, facility, database_form, fsID)
        return redirect(*template_validate_save(data, form_variables, *exportVariables))
    return render(request, "shared/forms/daily/form9.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'existing': existing, 
         
        'todays_log': todays_log, 
        'form': data, 
        'selector': selector,
        'formName': form_variables['formName'], 
        'leak_JSON': goose_neck_data_JSON, 
        'search': search, 
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq']
    })
