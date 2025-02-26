from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import daily_battery_profile_model, Forms, form5_model, form_settings_model, issues_model, bat_info_model
from ..forms import formA5_form, user_profile_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import parse_form5_oven_dict, form5_reading_data_build, formA5_ovens_data_build, getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, weatherDict, createNotification, get_initial_data

lock = login_required(login_url='Login')


@lock
def formA5(request, facility, fsID, selector):
    variables = {}
    formName = 5
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    submitted_forms = form5_model.objects.all().order_by('-date')
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
        if selector == 'new':
            existing = False
        elif selector != 'form':
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
        elif now == todays_log.date_save:
            if submitted_forms.exists():
                database_form = submitted_forms[0]
                if str(todays_log.date_save) == str(database_form.date):
                    existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)

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
                    'date': now,
                    'estab': options.facility_name,
                    'county': options.county,
                    'estab_no': options.estab_num,
                    'equip_loc': options.equip_location,
                    'district': options.district,
                    'city': options.city,
                    'observer': full_name,
                    'cert_date': cert_date,
                    'process_equip1': "Coke Battery / Door Machine / Hot Car",
                    'process_equip2': "Door Machine / PECS",
                    'op_mode1': "normal",
                    'op_mode2': "normal",
                    'emission_point_start': "Above hot car",
                    'emission_point_stop': "Above door machine hood",
                    'height_above_ground': options.bat_height,
                    'height_rel_observer': options.bat_height,
                    'plume_type': 'N/A',
                    'water_drolet_present': "No",
                    'water_droplet_plume': "N/A",
                    'plume_opacity_determined_start': "Above hot car",
                    'plume_opacity_determined_stop': "Above door machine hood",
                    'describe_background_start': "Skies",
                    'describe_background_stop': "Same",
                    #'sky_conditions': weather['description'],
                    'wind_speed_stop': 'TBD',
                    #'wind_direction': wind_direction,
                    'ambient_temp_stop': 'TBD',
                    #'humidity': weather['humidity'],
                }
                if selector == 'new':
                    initial_data['date'] = ''
                    initial_data['observer'] = ''
            data = formA5_form(initial=initial_data)
            variables['profile_form'] = user_profile_form()

        if request.method == "POST":
            dataCopy = request.POST.copy()
            dataCopy['ovens_data'] = formA5_ovens_data_build(request.POST)
            dataCopy['reading_data'] = form5_reading_data_build(request.POST)
            dataCopy['reading_data']['units'] = options.bat_height_label
            if existing:
                if request.POST['canvas'] == '' or 'canvas' not in request.POST.keys():
                    dataCopy['canvas'] = exist_canvas
                form = formA5_form(dataCopy, instance=database_form)
            else:
                form = formA5_form(dataCopy)
                
            A_valid = form.is_valid()
            finalFacility = options
            if A_valid:
                A = form.save(commit=False)
                A.formSettings = form_settings_model.objects.get(id=int(fsID))
                if not existing:
                    if A.reading_data['wind_speed_stop'] == 'TBD':
                        if int(A.reading_data['wind_speed_start']) == int(weather["wind_speed"]):
                            A.reading_data['wind_speed_stop'] = 'same'
                        else:
                            A.reading_data['wind_speed_stop'] = weather['wind_speed']
                    if A.reading_data['ambient_temp_stop'] == 'TBD':
                        if int(A.reading_data['ambient_temp_start']) == int(weather['temperature']):
                            A.reading_data['ambient_temp_stop'] = 'same'
                        else:
                            A.reading_data['ambient_temp_stop'] = weather['temperature']
                A.facilityChoice = finalFacility
                if not existing:
                    database_form = A
                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, formChoice=A.formSettings).exists()
                issueFound = False
                if float(A.ovens_data['oven1']['highest_opacity']) >= 10 or float(A.ovens_data['oven1']['average_6_opacity']) >= 35 or A.ovens_data['oven1']['opacity_over_20'] == 'Yes' or A.ovens_data['oven1']['average_6_over_35'] == 'Yes':
                    issueFound = True
                elif float(A.ovens_data['oven2']['highest_opacity']) >= 10 or float(A.ovens_data['oven2']['average_6_opacity']) >= 35 or A.ovens_data['oven2']['opacity_over_20'] == 'Yes' or A.ovens_data['oven2']['average_6_over_35'] == 'Yes':
                    issueFound = True
                elif float(A.ovens_data['oven3']['highest_opacity']) >= 10 or float(A.ovens_data['oven3']['average_6_opacity']) >= 35 or A.ovens_data['oven3']['opacity_over_20'] == 'Yes' or A.ovens_data['oven3']['average_6_over_35'] == 'Yes':
                    issueFound = True
                elif float(A.ovens_data['oven4']['highest_opacity']) >= 10 or float(A.ovens_data['oven4']['average_6_opacity']) >= 35 or A.ovens_data['oven4']['opacity_over_20'] == 'Yes' or A.ovens_data['oven4']['average_6_over_35'] == 'Yes':
                    issueFound = True
                A.save()
                
                if issueFound:
                    if finder:
                        if selector == 'form':
                            issue_page = 'resubmit'
                        else:
                            issue_page = 'issue'
                    else:
                        issue_page = 'form'
                    return redirect('issues_view', facility, fsID, str(database_form.date), issue_page)
                if selector != 'new':
                    createNotification(facility, request, fsID, now, 'submitted', False)
                    updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)

    variables.update({
        'picker': picker, 
        'weather': weather2, 
        "supervisor": supervisor, 
        "search": search, 
        "existing": existing, 
        "exist_canvas": exist_canvas, 
         
        'todays_log': todays_log, 
        'data': data, 
        'formName': formName, 
        'selector': selector, 
        'client': client, 
        'unlock': unlock, 
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'fsID': fsID,
        "options": options
    })
    return render(request, "shared/forms/daily/formA5.html", variables)
