from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime, timedelta
from ..models import form19_model, form19_readings_model
from ..forms import formH_form, formH_readings_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import formA19_Readings_Upadte, get_initial_data, getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, weatherDict, createNotification
from ..initial_form_variables import initiate_form_variables, existing_or_new_form

lock = login_required(login_url='Login')

@lock
def form19(request, facility, fsID, selector):
    formA19_Readings_Upadte()
    form_variables = initiate_form_variables(fsID, request.user, facility, selector)
    cert_date = request.user.user_profile_model.cert_date if request.user.user_profile_model else False
    personalizedSettings = form_variables['freq'].settings["settings"]
    start_saturday = form_variables['now'] - timedelta(days=form_variables['now'].weekday() + 2)
    end_friday = start_saturday + timedelta(days=6)
    org2 = form19_readings_model.objects.all().order_by('-form')
    orgFormL = org2.filter(comb_formL__exact=True)
    exist_canvas = ''
    # Weather API Pull
    weather = weatherDict(form_variables['freq'].facilityChoice.city)
    
    if form_variables['daily_prof'].exists():
        todays_log = form_variables['daily_prof'][0]
        data, existing, search = existing_or_new_form(todays_log, selector, form_variables['submitted_forms'], form_variables['now'], facility, request)
        if selector != 'form' and selector != 'formL':
            form_query = form_variables['submitted_forms'].filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            for x in org2:
                if str(x.form.date) == str(selector):
                    database_model2 = x
            readings_form = database_model2
            existing = True
            search = True
        elif form_variables['now'] == todays_log.date_save:
            if form_variables['submitted_forms'].exists() or org2.exists():
                if selector != 'formL':
                    database_form = form_variables['submitted_forms'][0]
                    database_form2 = org2[0]
                    # -------check if there is a daily battery profile
                    if start_saturday < database_form.date < end_friday:
                        existing = True
                elif orgFormL.exists():
                    formName = 'H-L'
                    database_form2 = orgFormL[0]
                    for line in form_variables['submitted_forms']:
                        if line.date == database_form2.form.date:
                            database_form = line
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
                initial_data = get_initial_data(form19_model, database_form)
                data = formH_form(initial=initial_data)
                readings_form = formH_readings_form(initial=initial_data)
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
                data = formH_form(initial=initial_data)
                readings_form = formH_readings_form()

        if request.method == "POST":
            if existing:
                if request.POST['canvas'] == '' or 'canvas' not in request.POST.keys():
                    dataCopy = request.POST.copy()
                    dataCopy['canvas'] = exist_canvas
                    form = formH_form(dataCopy, instance=database_form)
                else:
                    form = formH_form(request.POST, instance=database_form)
                readings = formH_readings_form(request.POST, instance=database_form2)
            else:
                form = formH_form(request.POST)
                readings = formH_readings_form(request.POST)
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
        batt_prof_date = str(form_variables['now'].year) + '-' + str(form_variables['now'].month) + '-' + str(form_variables['now'].day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/weekly/formH.html", {
        'fsID': fsID, 
        'picker': form_variables['picker'], 
        'facility': facility, 
        'notifs': form_variables['notifs'],
        'freq': form_variables['freq'],
        'selector': selector, 
        'weather': json.dumps(weather), 
        "exist_canvas": exist_canvas, 
        "supervisor": form_variables['supervisor'], 
        "search": search, 
        "existing": existing, 
         
        'data': data,
        'todays_log': todays_log, 
        'formName': form_variables['formName'], 
        'client': form_variables['client'], 
        'unlock': form_variables['unlock'], 
        'readings_form': readings_form,
        'options': form_variables['options']
    })