from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form5_model, form_settings_model
from ..forms import form5_form, user_profile_form
from ..utils.main_utils import parse_form5_oven_dict, method9_reading_data_build, formA5_ovens_data_build, weatherDict, get_initial_data
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json

lock = login_required(login_url='Login')

@lock
def form5(request, facility, fsID, selector):
    variables = {}
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    cert_date = request.user.user_profile.cert_date if request.user.user_profile else False
    exist_canvas = ''
    # Weather API Pull
    weather = weatherDict(form_variables['freq'].facilityChoice.city)
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
        if selector == 'new':
            existing = False
        if search:
            exist_canvas = data.canvas
        else:
            if existing:
                exist_canvas = database_form.canvas
                unparsedData = get_initial_data(form5_model, database_form)
                reading_data, ovens_data = parse_form5_oven_dict(unparsedData['reading_data'], unparsedData['ovens_data'])
                newData = reading_data | ovens_data
                initial_data = newData | unparsedData
            else:
                initial_data = {
                    'date': form_variables['now'],
                    'estab': form_variables['freq'].facilityChoice.facility_name,
                    'county': form_variables['freq'].facilityChoice.county,
                    'estab_no': form_variables['freq'].facilityChoice.estab_num,
                    'equip_loc': form_variables['freq'].facilityChoice.equip_location,
                    'district': form_variables['freq'].facilityChoice.district,
                    'city': form_variables['freq'].facilityChoice.city,
                    'observer': form_variables['full_name'],
                    'cert_date': cert_date,
                    'process_equip1': "Coke Battery / Door Machine / Hot Car",
                    'process_equip2': "Door Machine / PECS",
                    'op_mode1': "normal",
                    'op_mode2': "normal",
                    'emission_point_start': "Above hot car",
                    'emission_point_stop': "Above door machine hood",
                    'height_above_ground': form_variables['freq'].facilityChoice.bat_height,
                    'height_rel_observer': form_variables['freq'].facilityChoice.bat_height,
                    'plume_type': 'N/A',
                    'water_drolet_present': "No",
                    'water_droplet_plume': "N/A",
                    'plume_opacity_determined_start': "Above hot car",
                    'plume_opacity_determined_stop': "Above door machine hood",
                    'describe_background_start': "Skies",
                    'describe_background_stop': "Same",
                    'wind_speed_stop': 'TBD',
                    'ambient_temp_stop': 'TBD',
                }
                if selector == 'new':
                    initial_data['date'] = ''
                    initial_data['observer'] = ''
            data = form5_form(initial=initial_data, form_settings=form_variables['freq'])
            variables['profile_form'] = user_profile_form()
    # -----IF REQUEST.POST------------
        if request.method == "POST":
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS------------
            dataCopy = request.POST.copy()
            dataCopy['ovens_data'] = formA5_ovens_data_build(request.POST)
            dataCopy['reading_data'] = method9_reading_data_build(request.POST)
            dataCopy['reading_data']['units'] = form_variables['freq'].facilityChoice.bat_height_label
            
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
    # -----SET FORM VARIABLE IN RESPONSE TO DECIDING VARIABLES------------
            if existing:
                if request.POST['canvas'] == '' or 'canvas' not in request.POST.keys():
                    dataCopy['canvas'] = exist_canvas
                form = form5_form(dataCopy, instance=database_form, form_settings=form_settings)
            else:
                if dataCopy['reading_data']['wind_speed_stop'] == 'TBD':
                    if int(dataCopy['reading_data']['wind_speed_start']) == int(weather["wind_speed"]):
                        dataCopy['reading_data']['wind_speed_stop'] = 'same'
                    else:
                        dataCopy['reading_data']['wind_speed_stop'] = weather['wind_speed']
                if dataCopy['reading_data']['ambient_temp_stop'] == 'TBD':
                    if int(dataCopy['reading_data']['ambient_temp_start']) == int(weather['temperature']):
                        dataCopy['reading_data']['ambient_temp_stop'] = 'same'
                    else:
                        dataCopy['reading_data']['ambient_temp_stop'] = weather['temperature']
                form = form5_form(dataCopy, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    variables.update({
        'picker': form_variables['picker'], 
        'weather': json.dumps(weather),
        "supervisor": form_variables['supervisor'], 
        "search": search, 
        "existing": existing, 
        "exist_canvas": exist_canvas, 
         
        'todays_log': todays_log, 
        'data': data, 
        'formName': form_variables['formName'], 
        'selector': selector, 
        'client': form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'facility': facility,
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'fsID': fsID,
        "options": form_variables['freq'].facilityChoice
    })
    return render(request, "shared/forms/daily/form5.html", variables)
