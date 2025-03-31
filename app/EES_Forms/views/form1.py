from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect, JsonResponse  # type: ignore
from ..models import form_settings_model, daily_battery_profile_model, form1_model, form1_model
from ..forms import form1_form
from ..utils import form1_json_build, parse_form1_oven_dict, get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist # type: ignore

lock = login_required(login_url='Login')

@lock
def form1(request, facility, fsID, selector):
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
        else:
            if existing:
                unparsedData = get_initial_data(form1_model, database_form)
                ovens_data = parse_form1_oven_dict(unparsedData['ovens_data'])
                initial_data = unparsedData | ovens_data
                print(ovens_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': form_variables['full_name'],
                    'crew': todays_log.crew,
                    'foreman': todays_log.foreman,
                    'facility_name': facility,
                    'formSettings': form_settings_model.objects.get(id=int(fsID))
                }
            data = form1_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            copyPOST = request.POST.copy()
            copyPOST['ovens_data'] = form1_json_build(request.POST)

            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form1_form(copyPOST, instance=database_form, form_settings=form_settings)
            else:
                form = form1_form(copyPOST, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    return render(request, "shared/forms/daily/form1.html", {
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'supervisor': form_variables['supervisor'], 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'options': form_variables['freq'].facilityChoice, 
        "search": search, 
        'todays_log': todays_log, 
        'data': data, 
        'formName': form_variables['formName'], 
        'selector': selector,
        'picker': form_variables['picker'],
        'fsID': fsID
    })

def inop_check_form_1(request):  # Add request parameter
    today = datetime.now().date()
    try:
        dailyBatProf = daily_battery_profile_model.objects.get(date_save=today)

        # If `inop_numbs` is stored as a string like '44,45,54,62', split it into a list
        response_data = dailyBatProf.inop_numbs[1:-1].replace(" ", "").split(",") if dailyBatProf.inop_numbs != "[]" else []
    except ObjectDoesNotExist:
        response_data = []

    return JsonResponse(response_data, safe=False)

