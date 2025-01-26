from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, form19_model, form19_readings_model, bat_info_model
from ..forms import formH_form, user_profile_form, formH_readings_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import get_initial_data, getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, weatherDict, createNotification

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
                initial_data = get_initial_data(form19_model, database_form)
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