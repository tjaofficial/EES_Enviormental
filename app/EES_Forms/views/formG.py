from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, formG1_model, formG1_readings_model, formG2_model, user_profile_model, daily_battery_profile_model, formG2_readings_model
from ..forms import formG1_form, formG2_form, formG1_readings_form, formG2_readings_form, user_profile_form
import requests

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formG1(request, selector):
    formName = "G1"
    existing = False
    unlock = False
    client = False
    search = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    
    org = formG1_model.objects.all().order_by('-date')
    org2 = formG1_readings_model.objects.all().order_by('-form')
    
    count_bp = daily_battery_profile_model.objects.count()
    
    full_name = request.user.get_full_name()

    if len(profile) > 0:
        same_user = user_profile_model.objects.filter(user__exact=request.user.id)
        if same_user:
            cert_date = request.user.user_profile_model.cert_date
        else:
            return redirect('IncompleteForms')
    else:
        return redirect('IncompleteForms')
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'
    city = 'Dearborn'
    city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types
    weather = {
        'city': city,
        'temperature': round(city_weather['main']['temp'], 0),
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'wind_speed': round(city_weather['wind']['speed'], 0),
        'wind_direction': city_weather['wind']['deg'],
        'humidity': city_weather['main']['humidity'],
    }
    degree = weather['wind_direction']
    
    def toTextualDescription(degree):
        if degree > 337.5:
            return 'N'
        if degree > 292.5:
            return 'NW'
        if degree > 247.5:
            return 'W'
        if degree > 202.5:
            return 'SW'
        if degree > 157.5:
            return 'S'
        if degree > 122.5:
            return 'SE'
        if degree > 67.5:
            return 'E'
        if degree > 22.5:
            return 'NE'
        return 'N'
    wind_direction = toTextualDescription(degree)

    if count_bp != 0:
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
        elif len(org) > 0 or len(org2) > 0:
            database_form = org[0]
            database_form2 = org2[0]
            # -------check if there is a daily battery profile
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_form.date:
                        existing = True
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        
        if search:
            database_form = ''
        else:
            if existing:
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
                    
                    'PEC_push_oven': database_form2.PEC_push_oven,
                    'PEC_push_time': database_form2.PEC_push_time,
                    'PEC_observe_time': database_form2.PEC_observe_time,
                    'PEC_emissions_present': database_form2.PEC_emissions_present,
                }
                data = formG1_form(initial=initial_data)
                readings_form = formG1_readings_form(initial=initial_data)
                profile_form = user_profile_form()
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'estab': "EES COKE BATTERY",
                    'county': "Wayne",
                    'estab_no': "P0408",
                    'equip_loc': "Zug Island",
                    'district': "Detroit",
                    'city': "River Rouge",
                    'observer': full_name,
                    'cert_date': cert_date,
                    'process_equip1': "-",
                    'process_equip2': "-",
                    'op_mode1': "normal",
                    'op_mode2': "normal",
                    'emission_point_start': "Above Stack",
                    'emission_point_stop': "Same",
                    'height_above_ground': "300",
                    'height_rel_observer': "300",
                    'water_drolet_present': "No",
                    'water_droplet_plume': "N/A",
                    'describe_background_start': "Skies",
                    'describe_background_stop': "Same",
                    'sky_conditions': weather['description'],
                    'wind_speed_start': weather['wind_speed'],
                    'wind_direction': wind_direction,
                    'ambient_temp_start': weather['temperature'],
                    'humidity': weather['humidity'],
                }
                data = formG1_form(initial=initial_data)
                profile_form = user_profile_form()
                readings_form = formG1_readings_form()

        if request.method == "POST":
            if existing:
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
                
                A.save()

                B.form = A
                B.save()

                done = Forms.objects.filter(form='G-1')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
            else:
                print(form.errors)
                print(readings.errors)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formG1.html", {
        "admin": admin, "search": search, "existing": existing, 'client': client, 'unlock': unlock, 'readings_form': readings_form, "back": back, 'data': data, 'profile_form': profile_form,  'selector': selector, 'profile': profile, 'todays_log': todays_log, 'formName': formName
    })


@lock
def formG2(request, selector):
    formName = "G2"
    existing = False
    unlock = False
    client = False
    search = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    
    org = formG2_model.objects.all().order_by('-date')
    org2 = formG2_readings_model.objects.all().order_by('-form')
    
    count_bp = daily_battery_profile_model.objects.count()
    
    full_name = request.user.get_full_name()

    if len(profile) > 0:
        same_user = user_profile_model.objects.filter(user__exact=request.user.id)
        if same_user:
            cert_date = request.user.user_profile_model.cert_date
        else:
            return redirect('IncompleteForms')
    else:
        return redirect('IncompleteForms')
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'
    city = 'Dearborn'
    city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types
    weather = {
        'city': city,
        'temperature': round(city_weather['main']['temp'], 0),
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'wind_speed': round(city_weather['wind']['speed'], 0),
        'wind_direction': city_weather['wind']['deg'],
        'humidity': city_weather['main']['humidity'],
    }
    degree = weather['wind_direction']
    
    def toTextualDescription(degree):
        if degree > 337.5:
            return 'N'
        if degree > 292.5:
            return 'NW'
        if degree > 247.5:
            return 'W'
        if degree > 202.5:
            return 'SW'
        if degree > 157.5:
            return 'S'
        if degree > 122.5:
            return 'SE'
        if degree > 67.5:
            return 'E'
        if degree > 22.5:
            return 'NE'
        return 'N'
    wind_direction = toTextualDescription(degree)

    if count_bp != 0:
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
        elif len(org) > 0 or len(org2) > 0:
            database_form = org[0]
            database_form2 = org2[0]
            # -------check if there is a daily battery profile
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_form.date:
                        existing = True
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
        
        if search:
            database_form = ''
        else:
            if existing:
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

                    'PEC_oven_1': database_form2.PEC_oven_1,
                    'PEC_oven_2': database_form2.PEC_oven_2,
                    'PEC_oven_3': database_form2.PEC_oven_3,
                    'PEC_start_1': database_form2.PEC_start_1,
                    'PEC_start_2': database_form2.PEC_start_2,
                    'PEC_start_3': database_form2.PEC_start_3,
                    'PEC_average_1': database_form2.PEC_average_1,
                    'PEC_average_2': database_form2.PEC_average_2,
                    'PEC_average_3': database_form2.PEC_average_3,
                    'PEC_average_m': database_form2.PEC_average_m,
                }
                data = formG2_form(initial=initial_data)
                readings_form = formG2_readings_form(initial=initial_data)
                profile_form = user_profile_form()
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'estab': "EES COKE BATTERY",
                    'county': "Wayne",
                    'estab_no': "P0408",
                    'equip_loc': "Zug Island",
                    'district': "Detroit",
                    'city': "River Rouge",
                    'observer': full_name,
                    'cert_date': cert_date,
                    'process_equip1': "-",
                    'process_equip2': "-",
                    'op_mode1': "normal",
                    'op_mode2': "normal",
                    'emission_point_start': "Above Stack",
                    'emission_point_stop': "Same",
                    'height_above_ground': "300",
                    'height_rel_observer': "300",
                    'water_drolet_present': "No",
                    'water_droplet_plume': "N/A",
                    'describe_background_start': "Skies",
                    'describe_background_stop': "Same",
                    'sky_conditions': weather['description'],
                    'wind_speed_start': weather['wind_speed'],
                    'wind_direction': wind_direction,
                    'ambient_temp_start': weather['temperature'],
                    'humidity': weather['humidity'],
                }
                data = formG2_form(initial=initial_data)
                profile_form = user_profile_form()
                readings_form = formG2_readings_form()

        if request.method == "POST":
            if existing:
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
                
                A.save()

                B.form = A
                B.save()

                done = Forms.objects.filter(form='G-2')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
            else:
                print(form.errors)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Monthly/formG2.html", {
        "admin": admin, "search": search, "existing": existing, 'client': client, 'unlock': unlock, 'readings_form': readings_form, "back": back, 'data': data, 'profile_form': profile_form,  'selector': selector, 'profile': profile, 'todays_log': todays_log, 'formName': formName
    })
