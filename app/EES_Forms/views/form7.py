from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form7_model, form_settings_model
from ..forms import form7_form
from ..utils import parse_form7_oven_dict, get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json

lock = login_required(login_url='Login')

@lock
def form7(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    cert_date = request.user.user_profile.cert_date if request.user.user_profile else False
    # -----CHECK DAILY_BATTERY_PROF OR REDIRECT------------
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
    # -----SET DECIDING VARIABLES------------
        more_form_variables = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request, fsID) 
        if isinstance(more_form_variables, HttpResponseRedirect):
            return more_form_variables
        else:
            data, existing, search, database_form = more_form_variables
    # -----SET RESPONSES TO DECIDING VARIABLES------------
        if search:
            database_form = ''
            areaFilled1 = [str(x) for x in range(1,5) if getattr(data, f"area_json_{x}")]
        else:
            if existing:
                unparsedData = get_initial_data(form7_model, database_form)
                ovens_data = parse_form7_oven_dict(unparsedData['area_json_1'], unparsedData['area_json_2'], unparsedData['area_json_3'], unparsedData['area_json_4'])
                initial_data = unparsedData | ovens_data
                areaFilled1 = [str(x) for x in range(1,5) if getattr(database_form, f"area_json_{x}")]
            else:
                initial_data = {
                    'date': form_variables['now'].strftime("%Y-%m-%d"),
                    'observer': form_variables['full_name'],
                    'cert_date': cert_date.strftime("%Y-%m-%d"),
                }
                areaFilled1 = ["1","2","3","4"]
            data = form7_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
            print(request.POST)
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS/VARIABLES------------
            copyRequest = request.POST.copy()
            areaFilled = []
            for formKeys in request.POST.keys():
                areaNumb = formKeys[9:]
                areaKey = formKeys[:8]

                if areaKey == 'areaUsed':
                    if request.POST[formKeys] == "true":
                        areaFilled.append(areaNumb)
                        areaSetup = {
                            "selection": request.POST[f"{areaNumb}_selection"],
                            "start": request.POST[f"{areaNumb}_start"],
                            "stop": request.POST[f"{areaNumb}_stop"],
                            "readings": {
                                **{f"{i}": int(request.POST[f"{areaNumb}Read_{i}"]) for i in range(1,13)},
                            },
                            "average": float(request.POST[f'{areaNumb}_average'])
                        }
                        areaSetup = json.loads(json.dumps(areaSetup))
                        copyRequest[f'area_json_{areaNumb}'] = areaSetup
                    else:
                        copyRequest[f'area_json_{areaNumb}'] = dict()
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                form = form7_form(copyRequest, instance=database_form, form_settings=form_settings)
            else:
                form = form7_form(copyRequest, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/form7.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        "search": search, 
        "client": form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'supervisor': form_variables['supervisor'], 
        'selector': selector, 
        'formName': form_variables['formName'], 
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'existing': existing,
        'data': data,
        "areaFilled1": areaFilled1,
    })
