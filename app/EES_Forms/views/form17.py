from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from django.forms.models import model_to_dict # type: ignore
from ..models import form_settings_model, form17_model
from ..forms import form17_form
from ..utils.main_utils import get_initial_data, method9_reading_data_build, weatherDict, form17_ovens_data_build
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json

lock = login_required(login_url='Login')

@lock
def form17(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    cert_date = request.user.user_profile.cert_date if request.user.user_profile else False
    exist_canvas = ''
    # Weather API Pull
    weather = weatherDict(form_variables['freq'].facilityChoice.city)
    personalizedSettings = form_variables['freq'].settings["settings"]
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
            exist_canvas = data.canvas
            pecType = data.ovens_data["PEC_type"]
            paresedData = {"PEC_type": pecType}
            for key, iData in data.ovens_data[pecType].items():
                if key == "readings":
                    paresedData = paresedData | iData
                else:
                    paresedData[key] = iData
            data_dict = model_to_dict(data, exclude=['ovens_data', 'reading_data'])
            for key_2, iData_2 in data.reading_data.items():
                paresedData[key_2] = iData_2
            data = paresedData | data_dict
        else:
            if existing:
                exist_canvas = database_form.canvas
                unparsedData = get_initial_data(form17_model, database_form)
                initial_data = {
                    "reading_data": database_form.reading_data,
                    "ovens_data": database_form.ovens_data,
                }
                initial_data = initial_data | unparsedData
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
                    'process_equip1': personalizedSettings['process_equip1'],
                    'process_equip2': personalizedSettings['process_equip2'],
                    'op_mode1': personalizedSettings['operating_mode1'],
                    'op_mode2': personalizedSettings['operating_mode2'],
                    'emission_point_start': personalizedSettings['describe_emissions_point_start'],
                    'emission_point_stop': personalizedSettings['describe_emissions_point_stop'],
                    'height_above_ground': personalizedSettings['height_above_ground_level'],
                    'water_drolet_present': "No",
                    'water_droplet_plume': "N/A",
                    'describe_background_start': "Skies",
                    'describe_background_stop': "Same",
                    'wind_speed_stop': 'TBD',
                    'ambient_temp_stop': 'TBD',
                }
            data = form17_form(initial=initial_data, form_settings=form_variables['freq'])
    # -----IF REQUEST.POST------------
        if request.method == "POST":
            print(request.POST)
    # -----CREATE COPYPOST FOR ANY ADDITIONAL INPUTS------------
            dataCopy = request.POST.copy()
            dataCopy['ovens_data'] = form17_ovens_data_build(request.POST)
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
                form = form17_form(dataCopy, instance=database_form, form_settings=form_settings)
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
                form = form17_form(dataCopy, form_settings=form_settings)
    # -----VALIDATE, CHECK FOR ISSUES, CREATE NOTIF, UPDATE SUBMISSION FORM------------
            exportVariables = (request, selector, facility, database_form, fsID)
            return redirect(*template_validate_save(form, form_variables, *exportVariables))
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/weekly/form17.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        "exist_canvas": exist_canvas, 
        'weather': json.dumps(weather), 
        "supervisor": form_variables['supervisor'], 
        "search": search, 
        "existing": existing, 
        'client': form_variables['client'], 
        'unlock': form_variables['unlock'], 
         
        'data': data, 
        'selector': selector, 
        'todays_log': todays_log, 
        'formName': form_variables['formName'],
        'options': form_variables['freq'].facilityChoice
    })