from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import user_profile_model, daily_battery_profile_model, formB_model
from ..forms import Forms, formB_form
import requests
import json

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formB(request, facility, selector):
    formName = "B"
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
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    one_week = datetime.timedelta(days=4)
    end_week = last_monday + one_week
    freq = False
    if 2 < today.month < 11:
        freq = True
    week_start_dates = formB_model.objects.all().order_by('-week_start')

    count_bp = daily_battery_profile_model.objects.count()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=435ac45f81f3f8d42d164add25764f3c'
    city = 'Dearborn'
    city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types
    weather = {
        'wind_speed': round(city_weather['wind']['speed'], 0),
    }
    weather2 = json.dumps(weather)
    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in week_start_dates:
                if str(x.week_start) == str(selector):
                    database_model = x
            data = database_model
            existing = True
            search = True
            unlock = False
        elif len(week_start_dates) > 0:
            database_form = week_start_dates[0]
            if database_form.week_start == last_monday:
                existing = True
                    
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'week_start': database_form.week_start,
                    'week_end': database_form.week_end,
                    'observer_0': database_form.observer_0,
                    'time_0': database_form.time_0,
                    'weather_0': database_form.weather_0,
                    'wind_speed_0': database_form.wind_speed_0,
                    'fugitive_dust_observed_0': database_form.fugitive_dust_observed_0,
                    'supressant_applied_0': database_form.supressant_applied_0,
                    'supressant_active_0': database_form.supressant_active_0,
                    'working_face_exceed_0': database_form.working_face_exceed_0,
                    'spills_0': database_form.spills_0,
                    'pushed_back_0': database_form.pushed_back_0,
                    'coal_vessel_0': database_form.coal_vessel_0,
                    'water_sprays_0': database_form.water_sprays_0,
                    'loader_lowered_0': database_form.loader_lowered_0,
                    'working_water_sprays_0': database_form.working_water_sprays_0,
                    'barrier_thickness_0': database_form.barrier_thickness_0,
                    'surface_quality_0': database_form.surface_quality_0,
                    'surpressant_crust_0': database_form.surpressant_crust_0,
                    'additional_surpressant_0': database_form.additional_surpressant_0,
                    'comments_0': database_form.comments_0,
                    'wharf_0': database_form.wharf_0,
                    'breeze_0': database_form.breeze_0,

                    'observer_1': database_form.observer_1,
                    'time_1': database_form.time_1,
                    'weather_1': database_form.weather_1,
                    'wind_speed_1': database_form.wind_speed_1,
                    'fugitive_dust_observed_1': database_form.fugitive_dust_observed_1,
                    'supressant_applied_1': database_form.supressant_applied_1,
                    'supressant_active_1': database_form.supressant_active_1,
                    'working_face_exceed_1': database_form.working_face_exceed_1,
                    'spills_1': database_form.spills_1,
                    'pushed_back_1': database_form.pushed_back_1,
                    'coal_vessel_1': database_form.coal_vessel_1,
                    'water_sprays_1': database_form.water_sprays_1,
                    'loader_lowered_1': database_form.loader_lowered_1,
                    'working_water_sprays_1': database_form.working_water_sprays_1,
                    'barrier_thickness_1': database_form.barrier_thickness_1,
                    'surface_quality_1': database_form.surface_quality_1,
                    'surpressant_crust_1': database_form.surpressant_crust_1,
                    'additional_surpressant_1': database_form.additional_surpressant_1,
                    'comments_1': database_form.comments_1,
                    'wharf_1': database_form.wharf_1,
                    'breeze_1': database_form.breeze_1,

                    'observer_2': database_form.observer_2,
                    'time_2': database_form.time_2,
                    'weather_2': database_form.weather_2,
                    'wind_speed_2': database_form.wind_speed_2,
                    'fugitive_dust_observed_2': database_form.fugitive_dust_observed_2,
                    'supressant_applied_2': database_form.supressant_applied_2,
                    'supressant_active_2': database_form.supressant_active_2,
                    'working_face_exceed_2': database_form.working_face_exceed_2,
                    'spills_2': database_form.spills_2,
                    'pushed_back_2': database_form.pushed_back_2,
                    'coal_vessel_2': database_form.coal_vessel_2,
                    'water_sprays_2': database_form.water_sprays_2,
                    'loader_lowered_2': database_form.loader_lowered_2,
                    'working_water_sprays_2': database_form.working_water_sprays_2,
                    'barrier_thickness_2': database_form.barrier_thickness_2,
                    'surface_quality_2': database_form.surface_quality_2,
                    'surpressant_crust_2': database_form.surpressant_crust_2,
                    'additional_surpressant_2': database_form.additional_surpressant_2,
                    'comments_2': database_form.comments_2,
                    'wharf_2': database_form.wharf_2,
                    'breeze_2': database_form.breeze_2,

                    'observer_3': database_form.observer_3,
                    'time_3': database_form.time_3,
                    'weather_3': database_form.weather_3,
                    'wind_speed_3': database_form.wind_speed_3,
                    'fugitive_dust_observed_3': database_form.fugitive_dust_observed_3,
                    'supressant_applied_3': database_form.supressant_applied_3,
                    'supressant_active_3': database_form.supressant_active_3,
                    'working_face_exceed_3': database_form.working_face_exceed_3,
                    'spills_3': database_form.spills_3,
                    'pushed_back_3': database_form.pushed_back_3,
                    'coal_vessel_3': database_form.coal_vessel_3,
                    'water_sprays_3': database_form.water_sprays_3,
                    'loader_lowered_3': database_form.loader_lowered_3,
                    'working_water_sprays_3': database_form.working_water_sprays_3,
                    'barrier_thickness_3': database_form.barrier_thickness_3,
                    'surface_quality_3': database_form.surface_quality_3,
                    'surpressant_crust_3': database_form.surpressant_crust_3,
                    'additional_surpressant_3': database_form.additional_surpressant_3,
                    'comments_3': database_form.comments_3,
                    'wharf_3': database_form.wharf_3,
                    'breeze_3': database_form.breeze_3,

                    'observer_4': database_form.observer_4,
                    'time_4': database_form.time_4,
                    'weather_4': database_form.weather_4,
                    'wind_speed_4': database_form.wind_speed_4,
                    'fugitive_dust_observed_4': database_form.fugitive_dust_observed_4,
                    'supressant_applied_4': database_form.supressant_applied_4,
                    'supressant_active_4': database_form.supressant_active_4,
                    'working_face_exceed_4': database_form.working_face_exceed_4,
                    'spills_4': database_form.spills_4,
                    'pushed_back_4': database_form.pushed_back_4,
                    'coal_vessel_4': database_form.coal_vessel_4,
                    'water_sprays_4': database_form.water_sprays_4,
                    'loader_lowered_4': database_form.loader_lowered_4,
                    'working_water_sprays_4': database_form.working_water_sprays_4,
                    'barrier_thickness_4': database_form.barrier_thickness_4,
                    'surface_quality_4': database_form.surface_quality_4,
                    'surpressant_crust_4': database_form.surpressant_crust_4,
                    'additional_surpressant_4': database_form.additional_surpressant_4,
                    'comments_4': database_form.comments_4,
                    'wharf_4': database_form.wharf_4,
                    'breeze_4': database_form.breeze_4,
                }
            else:
                initial_data = {
                    'week_start': last_monday,
                    'week_end': end_week,
                }
            data = formB_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                data = formB_form(request.POST, instance=database_form)
            else:
                data = formB_form(request.POST)
            A_valid = data.is_valid()
            if A_valid:
                data.save()

                filled_out = True
                # for items in week_almost.whatever().values():
                #    if items == None:
                #        filled_out = False
                #        break
                if filled_out:
                    done = Forms.objects.filter(form='B')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()
                else:
                    done.submitted = False
                    done.save()
            return redirect('IncompleteForms', facility)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)
    return render(request, "Daily/formB.html", {
        'weather': weather2, "search": search, "client": client, 'unlock': unlock, 'admin': admin, "back": back, 'todays_log': todays_log, 'end_week': end_week, 'data': data, 'profile': profile, 'selector': selector, 'formName': formName, "freq": freq, 'facility': facility
    })
