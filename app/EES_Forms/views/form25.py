from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form25_model
from ..forms import form25_form, form25_form2
from ..utils.main_utils import get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import calendar

lock = login_required(login_url='Login')

@lock
def form25(request, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, selector)
    facility = form_variables['facilityName']
    questionLabels = {
        'q_1': 'Flow observed at monitoring location?',
        'q_2': 'Does the observed flow have an unnatural turbidity',
        'q_3': 'Does the observed flow have an unnatural color?',
        'q_4': 'Does the observed flow have an oil film?',
        'q_5': 'Does the observed flow have floating solids?',
        'q_6': 'Does the observed flow have foams?',
        'q_7': 'Does the observed flow have settleable solids?',
        'q_8': 'Does the observed flow have suspended solids?',
        'q_9': 'Does the observed flow have deposits?',
    }
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
            initial_data = get_initial_data(form25_model, database_form)
            additonal_data = {key: extra for key, extra in initial_data['data'].items()}
            initial_data = initial_data | additonal_data
            print(initial_data)
        else:
            initial_data = {
                'date': form_variables['now'],
                'observer': form_variables['full_name'],
            }
        data = form25_form2(initial=initial_data)
    # -----IF REQUEST.POST------------
    if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
        try:
            form_settings = form_variables['freq']
        except form_settings_model.DoesNotExist:
            raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
        copyPOST = request.POST.copy()
        requestQuestions = {f"q_{i}": request.POST.get(f"q_{i}") for i in range(1, 10)}
        copyPOST['data'] = {
            **requestQuestions,
            "comments": request.POST['comments'],
            "actions_taken": request.POST['actions_taken']
        }
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
        if existing:
            form = form25_form(copyPOST, instance=database_form, form_settings=form_settings)
        else:
            form = form25_form(copyPOST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
        exportVariables = (request, selector, facility, database_form, fsID)
        return redirect(*template_validate_save(form, form_variables, *exportVariables))
    return render(request, "shared/forms/weekly/form25.html", {
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
        'questionLabels': questionLabels
    })
