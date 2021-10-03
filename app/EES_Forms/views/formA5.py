from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import user_profile_model, daily_battery_profile_model, Forms, formA5_model, formA5_readings_model
from ..forms import formA5_form, formA5_readings_form, user_profile_form
import requests

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')
now = datetime.datetime.now()
today = datetime.date.today()


@lock
def formA5(request, selector):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    formName = "A5"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    org = formA5_model.objects.all().order_by('-date')
    org2 = formA5_readings_model.objects.all().order_by('-form')

    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date

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

    count_bp = daily_battery_profile_model.objects.count()

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
        else:
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    count1 = formA5_model.objects.count()
                    count2 = formA5_readings_model.objects.count()

                    if count1 and count2 != 0:
                        org = formA5_model.objects.all().order_by('-date')
                        database_form = org[0]
                        org2 = formA5_readings_model.objects.all().order_by('-form')
                        database_form2 = org2[0]
                        if str(todays_log.date_save) == str(database_form.date):
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
                                'o1': database_form2.o1,
                                'o1_start': database_form2.o1_start,
                                'o1_stop': database_form2.o1_stop,
                                'o1_highest_opacity': database_form2.o1_highest_opacity,
                                'o1_instant_over_20': database_form2.o1_instant_over_20,
                                'o1_average_6': database_form2.o1_average_6,
                                'o1_average_6_over_35': database_form2.o1_average_6_over_35,
                                'o2': database_form2.o2,
                                'o2_start': database_form2.o2_start,
                                'o2_stop': database_form2.o2_stop,
                                'o2_highest_opacity': database_form2.o2_highest_opacity,
                                'o2_instant_over_20': database_form2.o2_instant_over_20,
                                'o2_average_6': database_form2.o2_average_6,
                                'o2_average_6_over_35': database_form2.o2_average_6_over_35,
                                'o3': database_form2.o3,
                                'o3_start': database_form2.o3_start,
                                'o3_stop': database_form2.o3_stop,
                                'o3_highest_opacity': database_form2.o3_highest_opacity,
                                'o3_instant_over_20': database_form2.o3_instant_over_20,
                                'o3_average_6': database_form2.o3_average_6,
                                'o3_average_6_over_35': database_form2.o3_average_6_over_35,
                                'o4': database_form2.o4,
                                'o4_start': database_form2.o4_start,
                                'o4_stop': database_form2.o4_stop,
                                'o4_highest_opacity': database_form2.o4_highest_opacity,
                                'o4_instant_over_20': database_form2.o4_instant_over_20,
                                'o4_average_6': database_form2.o4_average_6,
                                'o4_average_6_over_35': database_form2.o4_average_6_over_35,
                                'o1_1_reads': database_form2.o1_1_reads,
                                'o1_2_reads': database_form2.o1_2_reads,
                                'o1_3_reads': database_form2.o1_3_reads,
                                'o1_4_reads': database_form2.o1_4_reads,
                                'o1_5_reads': database_form2.o1_5_reads,
                                'o1_6_reads': database_form2.o1_6_reads,
                                'o1_7_reads': database_form2.o1_7_reads,
                                'o1_8_reads': database_form2.o1_8_reads,
                                'o1_9_reads': database_form2.o1_9_reads,
                                'o1_10_reads': database_form2.o1_10_reads,
                                'o1_11_reads': database_form2.o1_11_reads,
                                'o1_12_reads': database_form2.o1_12_reads,
                                'o1_13_reads': database_form2.o1_13_reads,
                                'o1_14_reads': database_form2.o1_14_reads,
                                'o1_15_reads': database_form2.o1_15_reads,
                                'o1_16_reads': database_form2.o1_16_reads,
                                'o2_1_reads': database_form2.o2_1_reads,
                                'o2_2_reads': database_form2.o2_2_reads,
                                'o2_3_reads': database_form2.o2_3_reads,
                                'o2_4_reads': database_form2.o2_4_reads,
                                'o2_5_reads': database_form2.o2_5_reads,
                                'o2_6_reads': database_form2.o2_6_reads,
                                'o2_7_reads': database_form2.o2_7_reads,
                                'o2_8_reads': database_form2.o2_8_reads,
                                'o2_9_reads': database_form2.o2_9_reads,
                                'o2_10_reads': database_form2.o2_10_reads,
                                'o2_11_reads': database_form2.o2_11_reads,
                                'o2_12_reads': database_form2.o2_12_reads,
                                'o2_13_reads': database_form2.o2_13_reads,
                                'o2_14_reads': database_form2.o2_14_reads,
                                'o2_15_reads': database_form2.o2_15_reads,
                                'o2_16_reads': database_form2.o2_16_reads,
                                'o3_1_reads': database_form2.o3_1_reads,
                                'o3_2_reads': database_form2.o3_2_reads,
                                'o3_3_reads': database_form2.o3_3_reads,
                                'o3_4_reads': database_form2.o3_4_reads,
                                'o3_5_reads': database_form2.o3_5_reads,
                                'o3_6_reads': database_form2.o3_6_reads,
                                'o3_7_reads': database_form2.o3_7_reads,
                                'o3_8_reads': database_form2.o3_8_reads,
                                'o3_9_reads': database_form2.o3_9_reads,
                                'o3_10_reads': database_form2.o3_10_reads,
                                'o3_11_reads': database_form2.o3_11_reads,
                                'o3_12_reads': database_form2.o3_12_reads,
                                'o3_13_reads': database_form2.o3_13_reads,
                                'o3_14_reads': database_form2.o3_14_reads,
                                'o3_15_reads': database_form2.o3_15_reads,
                                'o3_16_reads': database_form2.o3_16_reads,
                                'o4_1_reads': database_form2.o4_1_reads,
                                'o4_2_reads': database_form2.o4_2_reads,
                                'o4_3_reads': database_form2.o4_3_reads,
                                'o4_4_reads': database_form2.o4_4_reads,
                                'o4_5_reads': database_form2.o4_5_reads,
                                'o4_6_reads': database_form2.o4_6_reads,
                                'o4_7_reads': database_form2.o4_7_reads,
                                'o4_8_reads': database_form2.o4_8_reads,
                                'o4_9_reads': database_form2.o4_9_reads,
                                'o4_10_reads': database_form2.o4_10_reads,
                                'o4_11_reads': database_form2.o4_11_reads,
                                'o4_12_reads': database_form2.o4_12_reads,
                                'o4_13_reads': database_form2.o4_13_reads,
                                'o4_14_reads': database_form2.o4_14_reads,
                                'o4_15_reads': database_form2.o4_15_reads,
                                'o4_16_reads': database_form2.o4_16_reads,
                                'notes': database_form.notes,
                            }
                            data = formA5_form(initial=initial_data)
                            readings_form = formA5_readings_form(initial=initial_data)
                            profile_form = user_profile_form()

                            if request.method == "POST":
                                form = formA5_form(request.POST, instance=database_form)
                                readings = formA5_readings_form(request.POST, instance=database_form2)
                                A_valid = form.is_valid()
                                B_valid = readings.is_valid()

                                if A_valid and B_valid:
                                    A = form.save()
                                    B = readings.save(commit=False)

                                    B.form = A
                                    B.save()

                                    if B.o1_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o1_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o1_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o1_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    done = Forms.objects.filter(form='A-5')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
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
                                'process_equip1': "Coke Battery / Door Machine / Hot Car",
                                'process_equip2': "Door Machine / PECS",
                                'op_mode1': "normal",
                                'op_mode2': "normal",
                                'emission_point_start': "Above hot car",
                                'emission_point_stop': "Above door machine hood",
                                'height_above_ground': "45",
                                'height_rel_observer': "45",
                                'plume_type': 'N/A',
                                'water_drolet_present': "No",
                                'water_droplet_plume': "N/A",
                                'plume_opacity_determined_start': "Above hot car",
                                'plume_opacity_determined_stop': "Above door machine hood",
                                'describe_background_start': "Skies",
                                'describe_background_stop': "Same",
                                'sky_conditions': weather['description'],
                                'wind_speed_start': weather['wind_speed'],
                                'wind_direction': wind_direction,
                                'ambient_temp_start': weather['temperature'],
                                'humidity': weather['humidity'],
                            }
                            data = formA5_form(initial=initial_data)
                            profile_form = user_profile_form()
                            readings_form = formA5_readings_form()

                            if request.method == "POST":
                                form = formA5_form(request.POST)
                                readings = formA5_readings_form(request.POST)
                                A_valid = form.is_valid()
                                B_valid = readings.is_valid()

                                if A_valid and B_valid:
                                    A = form.save()
                                    B = readings.save(commit=False)

                                    B.form = A
                                    B.save()

                                    if B.o1_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o1_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o1_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o1_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o2_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o3_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_highest_opacity >= 10:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_average_6 >= 35:
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_instant_over_20 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    if B.o4_average_6_over_35 == 'Yes':
                                        issue_page = '../../issues_view/A-5/' + str(database_form.date) + '/form'

                                        return redirect(issue_page)

                                    done = Forms.objects.filter(form='A-5')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                            else:
                                form = formA5_form(initial=initial_data)
                                readings_form = formA5_readings_form()
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
                            'process_equip1': "Coke Battery / Door Machine / Hot Car",
                            'process_equip2': "Door Machine / PECS",
                            'op_mode1': "normal",
                            'op_mode2': "normal",
                            'emission_point_start': "Above hot car",
                            'emission_point_stop': "Above door machine hood",
                            'height_above_ground': "45",
                            'height_rel_observer': "45",
                            'plume_type': 'N/A',
                            'water_drolet_present': "No",
                            'water_droplet_plume': "N/A",
                            'plume_opacity_determined_start': "Above hot car",
                            'plume_opacity_determined_stop': "Above door machine hood",
                            'describe_background_start': "Skies",
                            'describe_background_stop': "Same",
                            'sky_conditions': weather['description'],
                            'wind_speed_start': weather['wind_speed'],
                            'wind_direction': wind_direction,
                            'ambient_temp_start': weather['temperature'],
                            'humidity': weather['humidity'],
                        }
                        data = formA5_form(initial=initial_data)
                        profile_form = user_profile_form()
                        readings_form = formA5_readings_form()

                        if request.method == "POST":
                            form = formA5_form(request.POST)
                            readings = formA5_readings_form(request.POST)
                            A_valid = form.is_valid()
                            B_valid = readings.is_valid()

                            if A_valid and B_valid:
                                A = form.save()
                                B = readings.save(commit=False)

                                B.form = A
                                B.save()

                                if B.o1_highest_opacity >= 10:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o1_average_6 >= 35:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o1_instant_over_20 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o1_average_6_over_35 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o2_highest_opacity >= 10:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o2_average_6 >= 35:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o2_instant_over_20 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o2_average_6_over_35 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o3_highest_opacity >= 10:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o3_average_6 >= 35:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o3_instant_over_20 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o3_average_6_over_35 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o4_highest_opacity >= 10:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o4_average_6 >= 35:
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o4_instant_over_20 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                if B.o4_average_6_over_35 == 'Yes':
                                    issue_page = '../../issues_view/A-5/' + str(todays_log.date_save.date) + '/form'

                                    return redirect(issue_page)

                                done = Forms.objects.filter(form='A-5')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formA5.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'profile_form': profile_form, 'readings_form': readings_form, 'formName': formName, 'profile': profile, 'selector': selector, 'client': client, 'unlock': unlock,
    })
