from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect# type: ignore
from ..models import form_settings_model, form31_model
from ..forms import form31_form
from ..utils.main_utils import get_initial_data, fix_data
from ..initial_form_variables import template_validate_save, initiate_form_variables, existing_or_new_form
import json

lock = login_required(login_url='Login')

@lock
def form31(request, fsID, selector):
    fix_data(fsID)
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
    else:
        if existing:
            unparsedData = get_initial_data(form31_model, database_form)
            parsed_tank_data = {key: tank_input for key, tank_input in unparsedData['tank_json'].items()}
            initial_data = unparsedData | parsed_tank_data
        else:
            initial_data = {
                'date': todays_log.date_save,
                'observer': form_variables['full_name'],
                'formSettings': form_variables['freq'],
            }
        data = form31_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
    if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS------------
        try:
            form_settings = form_variables['freq']
        except form_settings_model.DoesNotExist:
            raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
        
        copyPOST = request.POST.copy()
        tank_data_json = {f"{tank_key}": f"{tank_data}" for tank_key, tank_data in request.POST.items() if tank_key not in ['csrfmiddlewaretoken','observer','date','time']}
        print(tank_data_json)
        copyPOST["tank_json"] = json.loads(json.dumps(tank_data_json))
        print(isinstance(copyPOST["tank_json"], dict))
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
        if existing:
            form = form31_form(copyPOST, instance=database_form, form_settings=form_settings)
        else:
            form = form31_form(copyPOST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
        exportVariables = (request, selector, facility, database_form, fsID)
        return redirect(*template_validate_save(form, form_variables, *exportVariables))
    return render(request, "shared/forms/Monthly/form31.html", {
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'supervisor': form_variables['supervisor'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'options': form_variables['options'], 
        "search": search, 
        'todays_log': todays_log, 
        'data': data, 
        'formName': form_variables['formName'], 
        'selector': selector,
        'picker': form_variables['picker'],
        'fsID': fsID,
        'existing': existing,
        "formSettings": form_variables['freq'].settings['settings']
    })