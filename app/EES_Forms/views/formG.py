from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import Forms, form17_model, form17_readings_model, form18_model, user_profile_model, daily_battery_profile_model, form18_readings_model, bat_info_model
from ..forms import formG1_form, formG2_form, formG1_readings_form, formG2_readings_form, user_profile_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, weatherDict, createNotification

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formG1(request, facility, fsID, selector):
    formName = 17
    freq = getFacSettingsInfo(fsID)
    personalizedSettings = freq.settings["settings"]
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.datetime.now().date()
    profile = user_profile_model.objects.filter(user__exact=request.user.id)
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    org = form17_model.objects.all().order_by('-date')
    org2 = form17_readings_model.objects.all().order_by('-form')
    full_name = request.user.get_full_name()
    exist_canvas = ''
    picker = issueForm_picker(facility, selector, fsID)
    
    if unlock:
        if profile.exists():
            cert_date = request.user.user_profile_model.cert_date
        else:
            return redirect('IncompleteForms', facility)
    
    # Weather API Pull
    weather = weatherDict(options.city)
    weather2 = json.dumps(weather)

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            print(str(selector))
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
                    break
            data = database_model
            for log in org2:
                print('hello')
                if str(log.form.date) == str(selector):
                    database_model2 = log
                    break
            readings_form = database_model2
            profile_form = ''
            existing = True
            search = True
        # ------check if database is empty----------
        elif org.exists() and org2.exists():
            database_form = org[0]
            database_form2 = org2[0]
            # -------check if there is a daily battery profile
            if now == todays_log.date_save:
                if todays_log.date_save == database_form.date:
                    existing = True
        
        if search:
            database_form = ''
            exist_canvas = data.canvas
        else:
            if existing:
                exist_canvas = database_form.canvas
                initial_data = {
                    'date': database_form.date,
                    'estab': database_form.estab,
                    'county': database_form.county,
                    'estab_no': database_form.estab_no,
                    'equip_loc': database_form.equip_loc,
                    'district': database_form.district,
                    'city': database_form.city,
                    'observer': database_form.observer,
                    'cert_date': database_form.cert_date,
                    'process_equip1': database_form.process_equip1,
                    'process_equip2': database_form.process_equip2,
                    'op_mode1': database_form.op_mode1,
                    'op_mode2': database_form.op_mode2,
                    'background_color_start': database_form.background_color_start,
                    'background_color_stop': database_form.background_color_stop,
                    'sky_conditions': database_form.sky_conditions,
                    'wind_speed_start': database_form.wind_speed_start,
                    'wind_speed_stop': database_form.wind_speed_stop,
                    'wind_direction': database_form.wind_direction,
                    'emission_point_start': database_form.emission_point_start,
                    'emission_point_stop': database_form.emission_point_stop,
                    'ambient_temp_start': database_form.ambient_temp_start,
                    'ambient_temp_stop': database_form.ambient_temp_stop,
                    'humidity': database_form.humidity,
                    'height_above_ground': database_form.height_above_ground,
                    'height_rel_observer': database_form.height_rel_observer,
                    'distance_from': database_form.distance_from,
                    'direction_from': database_form.direction_from,
                    'describe_emissions_start': database_form.describe_emissions_start,
                    'describe_emissions_stop': database_form.describe_emissions_stop,
                    'emission_color_start': database_form.emission_color_start,
                    'emission_color_stop': database_form.emission_color_stop,
                    'plume_type': database_form.plume_type,
                    'water_drolet_present': database_form.water_drolet_present,
                    'water_droplet_plume': database_form.water_droplet_plume,
                    'plume_opacity_determined_start': database_form.plume_opacity_determined_start,
                    'plume_opacity_determined_stop': database_form.plume_opacity_determined_stop,
                    'describe_background_start': database_form.describe_background_start,
                    'describe_background_stop': database_form.describe_background_stop,
                    
                    'PEC_start': database_form2.PEC_start,
                    'PEC_stop': database_form2.PEC_stop,
                    'PEC_read_1': database_form2.PEC_read_1,
                    'PEC_read_2': database_form2.PEC_read_2,
                    'PEC_read_3': database_form2.PEC_read_3,
                    'PEC_read_4': database_form2.PEC_read_4,
                    'PEC_read_5': database_form2.PEC_read_5,
                    'PEC_read_6': database_form2.PEC_read_6,
                    'PEC_read_7': database_form2.PEC_read_7,
                    'PEC_read_8': database_form2.PEC_read_8,
                    'PEC_read_9': database_form2.PEC_read_9,
                    'PEC_read_10': database_form2.PEC_read_10,
                    'PEC_read_11': database_form2.PEC_read_11,
                    'PEC_read_12': database_form2.PEC_read_12,
                    'PEC_read_13': database_form2.PEC_read_13,
                    'PEC_read_14': database_form2.PEC_read_14,
                    'PEC_read_15': database_form2.PEC_read_15,
                    'PEC_read_16': database_form2.PEC_read_16,
                    'PEC_read_17': database_form2.PEC_read_17,
                    'PEC_read_18': database_form2.PEC_read_18,
                    'PEC_read_19': database_form2.PEC_read_19,
                    'PEC_read_20': database_form2.PEC_read_20,
                    'PEC_read_21': database_form2.PEC_read_21,
                    'PEC_read_22': database_form2.PEC_read_22,
                    'PEC_read_23': database_form2.PEC_read_23,
                    'PEC_read_24': database_form2.PEC_read_24,

                    'PEC_average': database_form2.PEC_average,
                    'PEC_oven1' : database_form2.PEC_oven1,
                    'PEC_oven2' : database_form2.PEC_oven2,
                    'PEC_time1' : database_form2.PEC_time1,
                    'PEC_time2' : database_form2.PEC_time2,
                    'PEC_type' : database_form2.PEC_type,
                    'PEC_push_oven': database_form2.PEC_push_oven,
                    'PEC_push_time': database_form2.PEC_push_time,
                    'PEC_observe_time': database_form2.PEC_observe_time,
                    'PEC_emissions_present': database_form2.PEC_emissions_present,
                }
                readings_form = formG1_readings_form(initial=initial_data)
            else:
                initial_data = {
                    'date': now,
                    'estab': options.facility_name,
                    'county': options.county,
                    'estab_no': options.estab_num,
                    'equip_loc': options.equip_location,
                    'district': options.district,
                    'city': options.city,
                    'observer': full_name,
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
            data = formG1_form(initial=initial_data)
            profile_form = user_profile_form()

        if request.method == "POST":
            if existing:
                if request.POST['canvas'] == '' or 'canvas' not in request.POST.keys():
                    dataCopy = request.POST.copy()
                    dataCopy['canvas'] = exist_canvas
                    form = formG1_form(dataCopy, instance=database_form)
                form = formG1_form(request.POST, instance=database_form)
                readings = formG1_readings_form(request.POST, instance=database_form2)
            else:
                form = formG1_form(request.POST)
                readings = formG1_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = readings.is_valid()
            
            if A_valid and B_valid:
                A = form.save(commit=False)
                B = readings.save(commit=False)
                A.facilityChoice = options
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
                createNotification(facility, request, fsID, now, 'submitted', False)
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
            else:
                print(form.errors)
                print(readings.errors)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/weekly/formG1.html", {
        'fsID': fsID, 
        'picker': picker, 
        'facility': facility, 
        'notifs': notifs,
        'freq': freq,
        "exist_canvas": exist_canvas, 
        'weather': weather2, 
        "supervisor": supervisor, 
        "search": search, 
        "existing": existing, 
        'client': client, 
        'unlock': unlock, 
        'readings_form': readings_form, 
        "back": back, 
        'data': data, 
        'profile_form': profile_form, 
        'selector': selector, 
        'todays_log': todays_log, 
        'formName': formName,
        'options': options
    })

@lock
def formG2(request, facility, fsID, selector):
    formName = 18
    freq = getFacSettingsInfo(fsID)
    personalizedSettings = freq.settings["settings"]
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.datetime.now().date()
    userProf = request.user.user_profile_model
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    org = form18_model.objects.all().order_by('-date')
    org2 = form18_readings_model.objects.all().order_by('-form')
    full_name = request.user.get_full_name()
    exist_canvas = ''
    picker = issueForm_picker(facility, selector, fsID)
    
    if unlock:
        cert_date = request.user.user_profile_model.cert_date
    
    # Weather API Pull
    weather = weatherDict(options.city)
    weather2 = json.dumps(weather)

    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            for x in org2:
                if str(x.form.date) == str(selector):
                    database_model2 = x
            readings_form = database_model2
            profile_form = ''
            existing = True
            search = True
        # ------check if database is empty----------
        elif org.exists() or org2.exists():
            database_form = org[0]
            database_form2 = org2[0]
            # -------check if there is a daily battery profile
            if now == todays_log.date_save:
                if todays_log.date_save.month == database_form.date.month:
                    existing = True
        if search:
            database_form = ''
            exist_canvas = data.canvas
        else:
            if existing:
                exist_canvas = database_form.canvas
                initial_data = {
                    'date': database_form.date,
                    'estab': database_form.estab,
                    'county': database_form.county,
                    'estab_no': database_form.estab_no,
                    'equip_loc': database_form.equip_loc,
                    'district': database_form.district,
                    'city': database_form.city,
                    'observer': database_form.observer,
                    'cert_date': database_form.cert_date,
                    'process_equip1': database_form.process_equip1,
                    'process_equip2': database_form.process_equip2,
                    'op_mode1': database_form.op_mode1,
                    'op_mode2': database_form.op_mode2,
                    'background_color_start': database_form.background_color_start,
                    'background_color_stop': database_form.background_color_stop,
                    'sky_conditions': database_form.sky_conditions,
                    'wind_speed_start': database_form.wind_speed_start,
                    'wind_speed_stop': database_form.wind_speed_stop,
                    'wind_direction': database_form.wind_direction,
                    'emission_point_start': database_form.emission_point_start,
                    'emission_point_stop': database_form.emission_point_stop,
                    'ambient_temp_start': database_form.ambient_temp_start,
                    'ambient_temp_stop': database_form.ambient_temp_stop,
                    'humidity': database_form.humidity,
                    'height_above_ground': database_form.height_above_ground,
                    'height_rel_observer': database_form.height_rel_observer,
                    'distance_from': database_form.distance_from,
                    'direction_from': database_form.direction_from,
                    'describe_emissions_start': database_form.describe_emissions_start,
                    'describe_emissions_stop': database_form.describe_emissions_stop,
                    'emission_color_start': database_form.emission_color_start,
                    'emission_color_stop': database_form.emission_color_stop,
                    'plume_type': database_form.plume_type,
                    'water_drolet_present': database_form.water_drolet_present,
                    'water_droplet_plume': database_form.water_droplet_plume,
                    'plume_opacity_determined_start': database_form.plume_opacity_determined_start,
                    'plume_opacity_determined_stop': database_form.plume_opacity_determined_stop,
                    'describe_background_start': database_form.describe_background_start,
                    'describe_background_stop': database_form.describe_background_stop,

                    'PEC_read_a_1': database_form2.PEC_read_a_1,
                    'PEC_read_a_2': database_form2.PEC_read_a_2,
                    'PEC_read_a_3': database_form2.PEC_read_a_3,
                    'PEC_read_a_4': database_form2.PEC_read_a_4,
                    'PEC_read_a_5': database_form2.PEC_read_a_5,
                    'PEC_read_a_6': database_form2.PEC_read_a_6,
                    'PEC_read_a_7': database_form2.PEC_read_a_7,
                    'PEC_read_a_8': database_form2.PEC_read_a_8,
                    
                    'PEC_read_b_1': database_form2.PEC_read_b_1,
                    'PEC_read_b_2': database_form2.PEC_read_b_2,
                    'PEC_read_b_3': database_form2.PEC_read_b_3,
                    'PEC_read_b_4': database_form2.PEC_read_b_4,
                    'PEC_read_b_5': database_form2.PEC_read_b_5,
                    'PEC_read_b_6': database_form2.PEC_read_b_6,
                    'PEC_read_b_7': database_form2.PEC_read_b_7,
                    'PEC_read_b_8': database_form2.PEC_read_b_8,
                    
                    'PEC_read_c_1': database_form2.PEC_read_c_1,
                    'PEC_read_c_2': database_form2.PEC_read_c_2,
                    'PEC_read_c_3': database_form2.PEC_read_c_3,
                    'PEC_read_c_4': database_form2.PEC_read_c_4,
                    'PEC_read_c_5': database_form2.PEC_read_c_5,
                    'PEC_read_c_6': database_form2.PEC_read_c_6,
                    'PEC_read_c_7': database_form2.PEC_read_c_7,
                    'PEC_read_c_8': database_form2.PEC_read_c_8,

                    'PEC_oven_a': database_form2.PEC_oven_a,
                    'PEC_oven_b': database_form2.PEC_oven_b,
                    'PEC_oven_c': database_form2.PEC_oven_c,
                    'PEC_start_a': database_form2.PEC_start_a,
                    'PEC_start_b': database_form2.PEC_start_b,
                    'PEC_start_c': database_form2.PEC_start_c,
                    'PEC_average_a': database_form2.PEC_average_a,
                    'PEC_average_b': database_form2.PEC_average_b,
                    'PEC_average_c': database_form2.PEC_average_c,
                    'PEC_average_main': database_form2.PEC_average_main,
                }
                data = formG2_form(initial=initial_data)
                readings_form = formG2_readings_form(initial=initial_data)
                profile_form = user_profile_form()
            else:
                initial_data = {
                    'date': now,
                    'estab': options.facility_name,
                    'county': options.county,
                    'estab_no': options.estab_num,
                    'equip_loc': options.equip_location,
                    'district': options.district,
                    'city': options.city,
                    'observer': full_name,
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
                data = formG2_form(initial=initial_data)
                profile_form = user_profile_form()
                readings_form = formG2_readings_form()

        if request.method == "POST":
            if existing:
                if request.POST['canvas'] == '' or 'canvas' not in request.POST.keys():
                    dataCopy = request.POST.copy()
                    dataCopy['canvas'] = exist_canvas
                    form = formG2_form(dataCopy, instance=database_form)
                form = formG2_form(request.POST, instance=database_form)
                readings = formG2_readings_form(request.POST, instance=database_form2)
            else:
                form = formG2_form(request.POST)
                readings = formG2_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = readings.is_valid()
            
            if A_valid and B_valid:
                A = form.save(commit=False)
                B = readings.save(commit=False)
                A.facilityChoice = options
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
                createNotification(facility, request, fsID, now, 'submitted', False)
                updateSubmissionForm(fsID, True, todays_log.date_save)

                return redirect('IncompleteForms', facility)
            else:
                print(form.errors)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/monthly/formG2.html", {
        'fsID': fsID, 
        'picker': picker, 
        "exist_canvas": exist_canvas, 
        'weather': weather2, 
        "supervisor": supervisor, 
        "search": search, 
        "existing": existing, 
        'client': client, 
        'unlock': unlock, 
        'readings_form': readings_form, 
        "back": back, 
        'data': data, 
        'profile_form': profile_form, 
        'selector': selector, 
        'todays_log': todays_log, 
        'formName': formName, 
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'options': options
    })
