from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from ..models import form_settings_model, form17_model, form17_readings_model
from ..forms import form17_form, formG1_readings_form
from ..utils import formA17_Model_Upadte, get_initial_data, updateSubmissionForm, weatherDict, createNotification
from ..initial_form_variables import initiate_form_variables, existing_or_new_form, template_validate_save
import json
from datetime import datetime

lock = login_required(login_url='Login')

@lock
def form17(request, facility, fsID, selector):
    # -----SET MAIN VARIABLES------------
    formA17_Model_Upadte()
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    cert_date = request.user.user_profile_model.cert_date if request.user.user_profile_model else False
    org2 = form17_readings_model.objects.all().order_by('-form')
    personalizedSettings = form_variables['freq'].settings["settings"]
    exist_canvas = ''
    # Weather API Pull
    weather = weatherDict(form_variables['freq'].facilityChoice.city)

    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
        data, existing, search = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request)
        if selector != 'form':
            form_query = form_variables['submitted_forms'].filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            for log in org2:
                if str(log.form.date) == str(selector):
                    database_model2 = log
                    break
            readings_form = database_model2
            existing = True
            search = True
        # ------check if database is empty----------
        elif form_variables['now'] == todays_log.date_save:
            if form_variables['submitted_forms'].exists() and org2.exists():
                database_form = form_variables['submitted_forms'][0]
                database_form2 = org2[0]
            # -------check if there is a daily battery profile
                if todays_log.date_save == database_form.date:
                    existing = True
        else:
            batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
            exist_canvas = data.canvas
        else:
            if existing:
                exist_canvas = database_form.canvas
                initial_data = get_initial_data(form17_model, database_form)
                readings_form = formG1_readings_form(initial=initial_data)
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
                    #'sky_conditions': weather['description'],
                    'wind_speed_stop': 'TBD',
                    #'wind_direction': wind_direction,
                    'ambient_temp_stop': 'TBD',
                    #'humidity': weather['humidity'],
                }
                readings_form = formG1_readings_form()
            data = form17_form(initial=initial_data)

        if request.method == "POST":
            try:
                form_settings = form_variables['freq']
            except form_settings_model.DoesNotExist:
                raise ValueError(f"Error: form_settings_model with ID {fsID} does not exist.")
            
            if existing:
                if request.POST['canvas'] == '' or 'canvas' not in request.POST.keys():
                    dataCopy = request.POST.copy()
                    dataCopy['canvas'] = exist_canvas
                    form = form17_form(dataCopy, instance=database_form, form_settings=form_settings)
                form = form17_form(request.POST, instance=database_form, form_settings=form_settings)
                readings = formG1_readings_form(request.POST, instance=database_form2)
            else:
                form = form17_form(request.POST, form_settings=form_settings)
                readings = formG1_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = readings.is_valid()
            
            if A_valid and B_valid:
                A = form.save(commit=False)
                B = readings.save(commit=False)
                A.formSettings = form_variables['freq']
                if not existing:
                    if A.wind_speed_stop == 'TBD':
                        if int(A.wind_speed_start) == int(weather['wind_speed']):
                            A.wind_speed_stop = 'same'
                        else:
                            A.wind_speed_stop = weather['wind_speed']
                    if A.ambient_temp_stop == 'TBD':
                        if int(A.ambient_temp_start) == int(weather['temperature']):
                            A.ambient_temp_stop = 'same'
                        else:
                            A.ambient_temp_stop = weather['temperature']
                        
                A.save()

                B.form = A
                B.save()
                createNotification(facility, request, fsID, form_variables['now'], 'submitted', False)
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
            else:
                print(form.errors)
                print(readings.errors)
    else:
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/weekly/formG1.html", {
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
        'readings_form': readings_form, 
         
        'data': data, 
        'selector': selector, 
        'todays_log': todays_log, 
        'formName': form_variables['formName'],
        'options': form_variables['freq'].facilityChoice
    })