from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import user_profile_model, daily_battery_profile_model, Forms, form5_model, form5_readings_model, issues_model, bat_info_model
from ..forms import formA5_form, formA5_readings_form, user_profile_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor, weatherDict, createNotification

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

@lock
def formA5(request, facility, fsID, selector):
    formName = 5
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.datetime.now().date()
    profile = request.user.user_profile_model
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    org = form5_model.objects.all().order_by('-date')
    org2 = form5_readings_model.objects.all().order_by('-form')
    full_name = request.user.get_full_name()
    exist_canvas = ''
    picker = issueForm_picker(facility, selector, fsID)
    fields1 = [field1_1.name for field1_1 in form5_model._meta.get_fields()]
    fields2 = [field1_2.name for field1_2 in form5_readings_model._meta.get_fields()]
    print(fields2)
    if unlock:
        cert_date = request.user.user_profile_model.cert_date
    
    #Weather API Pull
    weather = weatherDict(options.city)
    print(weather['sunrise'])
    print(weather['sunset'])
    weather2 = json.dumps(weather)
    
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector == 'new':
            existing = False
        elif selector != 'form':
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
        elif org.exists() or org2.exists():
            database_form = org[0]
            database_form2 = org2[0]
            if now == todays_log.date_save:
                if str(todays_log.date_save) == str(database_form.date):
                    existing = True

        if search:
            database_form = ''
            exist_canvas = data.canvas
        else:
            if existing:
                exist_canvas = database_form.canvas
                initial_data = {}
                for field1 in fields1:
                    initial_data[field1] = getattr(database_form, field1)
                for field2 in fields2:
                    if field2 != 'pt_admin1_model':
                        initial_data[field2] = getattr(database_form2, field2)
                data = formA5_form(initial=initial_data)
                readings_form = formA5_readings_form(initial=initial_data)
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
                profile_form = user_profile_form()
                readings_form = formA5_readings_form()

        if request.method == "POST":
            if existing:
                if request.POST['canvas'] == '' or 'canvas' not in request.POST.keys():
                    dataCopy = request.POST.copy()
                    dataCopy['canvas'] = exist_canvas
                    form = formA5_form(dataCopy, instance=database_form)
                form = formA5_form(request.POST, instance=database_form)
                readings = formA5_readings_form(request.POST, instance=database_form2)
            else:
                form = formA5_form(request.POST)
                readings = formA5_readings_form(request.POST)
                
            A_valid = form.is_valid()
            B_valid = readings.is_valid()
            finalFacility = options
            if A_valid and B_valid:
                A = form.save(commit=False)
                B = readings.save(commit=False)
                print(A.date)

                if not existing:
                    print(A.wind_speed_stop)
                    print(weather['wind_speed'])
                    if A.wind_speed_stop == 'TBD':
                        if int(A.wind_speed_start) == int(weather["wind_speed"]):
                            A.wind_speed_stop = 'same'
                        else:
                            A.wind_speed_stop = weather['wind_speed']
                    if A.ambient_temp_stop == 'TBD':
                        if int(A.ambient_temp_start) == int(weather['temperature']):
                            A.ambient_temp_stop = 'same'
                        else:
                            A.ambient_temp_stop = weather['temperature']
                A.facilityChoice = finalFacility
                A.save()
                B.form = A
                B.save()
                
                if not existing:
                    database_form = A
                fsID = str(fsID)
                finder = issues_model.objects.filter(date=A.date, form=fsID).exists()
                issueFound = False
                if B.o1_highest_opacity >= 10 or B.o1_average_6 >= 35 or B.o1_instant_over_20 == 'Yes' or B.o1_average_6_over_35 == 'Yes':
                    issueFound = True
                elif B.o2_highest_opacity >= 10 or B.o2_average_6 >= 35 or B.o2_instant_over_20 == 'Yes'  or B.o2_average_6_over_35 == 'Yes':
                    issueFound = True
                elif B.o3_highest_opacity >= 10 or B.o3_average_6 >= 35 or B.o3_instant_over_20 == 'Yes' or B.o3_average_6_over_35 == 'Yes':
                    issueFound = True
                elif B.o4_highest_opacity >= 10 or B.o4_average_6 >= 35 or B.o4_instant_over_20 == 'Yes' or B.o4_average_6_over_35 == 'Yes':
                    issueFound = True
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
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "shared/forms/daily/formA5.html", {
        'picker': picker, 
        'weather': weather2, 
        "supervisor": supervisor, 
        "search": search, 
        "existing": existing, 
        "exist_canvas": exist_canvas, 
        "back": back, 
        'todays_log': todays_log, 
        'data': data, 
        'profile_form': profile_form, 
        'readings_form': readings_form, 
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
