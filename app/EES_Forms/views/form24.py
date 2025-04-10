from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form24_model
from ..forms import form24_form
from ..utils import fix_data, get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import calendar

lock = login_required(login_url='Login')

@lock
def form24(request, facility, fsID, selector, weekend_day):
    fix_data(fsID)
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    month_name = calendar.month_name[form_variables['now'].month]
    if weekend_day == 'saturday':
        ss_filler = 5
    elif weekend_day == 'sunday':
        ss_filler = 6
    else:
        ss_filler = ''
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
                initial_data = get_initial_data(form24_model, database_form)
            else:
                initial_data = {
                    'date': form_variables['now'],
                    'observer': form_variables['full_name'],
                    'month': month_name,
                    'weekend_day': ss_filler,
                }
            data = form24_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form24_form(request.POST, instance=database_form, form_settings=form_settings)
            else:
                form = form24_form(request.POST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', 'login', batt_prof_date)
    return render(request, "shared/forms/weekly/form24.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'data': data, 
        "search": search, 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'formName': form_variables['formName'], 
        'selector': selector,
        'weekend_day': weekend_day
    })
