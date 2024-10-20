from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, form19_model, form19_readings_model, bat_info_model
from ..forms import formH_form, user_profile_form, formH_readings_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, weatherDict, createNotification

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formH(request, facility, fsID, selector):
    formName = 19
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
    today = datetime.date.today()
    start_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    end_friday = start_saturday + datetime.timedelta(days=6)
    org = form19_model.objects.all().order_by('-date')
    org2 = form19_readings_model.objects.all().order_by('-form')
    orgFormL = org2.filter(comb_formL__exact=True)
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
        if selector != 'form' and selector != 'formL':
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
            if selector != 'formL':
                database_form = org[0]
                database_form2 = org2[0]
                # -------check if there is a daily battery profile
                if now == todays_log.date_save:
                    if start_saturday < database_form.date < end_friday:
                        existing = True
            elif orgFormL.exists():
                formName = 'H-L'
                database_form2 = orgFormL[0]
                for line in org:
                    if line.date == database_form2.form.date:
                        database_form = line
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
                    
                    'comb_start': database_form2.comb_start,
                    'comb_stop': database_form2.comb_stop,
                    'comb_read_1': database_form2.comb_read_1,
                    'comb_read_2': database_form2.comb_read_2,
                    'comb_read_3': database_form2.comb_read_3,
                    'comb_read_4': database_form2.comb_read_4,
                    'comb_read_5': database_form2.comb_read_5,
                    'comb_read_6': database_form2.comb_read_6,
                    'comb_read_7': database_form2.comb_read_7,
                    'comb_read_8': database_form2.comb_read_8,
                    'comb_read_9': database_form2.comb_read_9,
                    'comb_read_10': database_form2.comb_read_10,
                    'comb_read_11': database_form2.comb_read_11,
                    'comb_read_12': database_form2.comb_read_12,
                    'comb_read_13': database_form2.comb_read_13,
                    'comb_read_14': database_form2.comb_read_14,
                    'comb_read_15': database_form2.comb_read_15,
                    'comb_read_16': database_form2.comb_read_16,
                    'comb_read_17': database_form2.comb_read_17,
                    'comb_read_18': database_form2.comb_read_18,
                    'comb_read_19': database_form2.comb_read_19,
                    'comb_read_20': database_form2.comb_read_20,
                    'comb_read_21': database_form2.comb_read_21,
                    'comb_read_22': database_form2.comb_read_22,
                    'comb_read_23': database_form2.comb_read_23,
                    'comb_read_24': database_form2.comb_read_24,
                    'comb_read_25': database_form2.comb_read_25,
                    'comb_read_26': database_form2.comb_read_26,
                    'comb_read_27': database_form2.comb_read_27,
                    'comb_read_28': database_form2.comb_read_28,
                    'comb_read_29': database_form2.comb_read_29,
                    'comb_read_30': database_form2.comb_read_30,
                    'comb_read_31': database_form2.comb_read_31,
                    'comb_read_32': database_form2.comb_read_32,
                    'comb_read_33': database_form2.comb_read_33,
                    'comb_read_34': database_form2.comb_read_34,
                    'comb_read_35': database_form2.comb_read_35,
                    'comb_read_36': database_form2.comb_read_36,
                    'comb_read_37': database_form2.comb_read_37,
                    'comb_read_38': database_form2.comb_read_38,
                    'comb_read_39': database_form2.comb_read_39,
                    'comb_read_40': database_form2.comb_read_40,
                    'comb_read_41': database_form2.comb_read_41,
                    'comb_read_42': database_form2.comb_read_42,
                    'comb_read_43': database_form2.comb_read_43,
                    'comb_read_44': database_form2.comb_read_44,
                    'comb_read_45': database_form2.comb_read_45,
                    'comb_read_46': database_form2.comb_read_46,
                    'comb_read_47': database_form2.comb_read_47,
                    'comb_read_48': database_form2.comb_read_48,
                    'comb_read_49': database_form2.comb_read_49,
                    'comb_read_50': database_form2.comb_read_50,
                    'comb_read_51': database_form2.comb_read_51,
                    'comb_read_52': database_form2.comb_read_52,
                    'comb_read_53': database_form2.comb_read_53,
                    'comb_read_54': database_form2.comb_read_54,
                    'comb_read_55': database_form2.comb_read_55,
                    'comb_read_56': database_form2.comb_read_56,
                    'comb_read_57': database_form2.comb_read_57,
                    'comb_read_58': database_form2.comb_read_58,
                    'comb_read_59': database_form2.comb_read_59,
                    'comb_read_60': database_form2.comb_read_60,
                    'comb_average': database_form2.comb_average,
                }
                data = formH_form(initial=initial_data)
                readings_form = formH_readings_form(initial=initial_data)
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
                data = formH_form(initial=initial_data)
                profile_form = user_profile_form()
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
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/weekly/formH.html", {
        'fsID': fsID, 
        'picker': picker, 
        'facility': facility, 
        'notifs': notifs,
        'freq': freq,
        'selector': selector, 
        'weather': weather2, 
        "exist_canvas": exist_canvas, 
        "supervisor": supervisor, 
        "search": search, 
        "existing": existing, 
        "back": back, 
        'data': data, 
        'profile_form': profile_form, 
        'profile': profile, 
        'todays_log': todays_log, 
        'formName': formName, 
        'client': client, 
        'unlock': unlock, 
        'readings_form': readings_form,
        'options': options
    })