from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime, date, timedelta
from ..models import user_profile_model, daily_battery_profile_model, form6_model, bat_info_model, formSubmissionRecords_model
from ..forms import Forms, formB_form
import json
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker, updateSubmissionForm, setUnlockClientSupervisor, weatherDict, createNotification, get_initial_data

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

@lock
def formB(request, facility, fsID, selector):
    formName = 6
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    week_start_dates = form6_model.objects.filter(facilityChoice__facility_name=facility).order_by('-week_start')
    profile = user_profile_model.objects.all()
    today = date.today()
    picker = issueForm_picker(facility, selector, fsID)
    last_monday = today - timedelta(days=today.weekday())
    one_week = timedelta(days=4)
    end_week = last_monday + one_week
    freq2 = False
    fridayDate = today + timedelta(days=(4 - today.weekday()))
    if 2 < today.month < 11:
        freq2 = True
    elif today.month == 2 and fridayDate.month == (today.month + 1):
        freq2 = True
    elif today.month == 10 and fridayDate.month == (today.month + 1):
        freq2 = True


    # Weather API Pull
    weather = weatherDict(options.city)
    weather2 = json.dumps(weather)
    
    
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            form_query = week_start_dates.filter(week_start=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
        elif len(week_start_dates) > 0:
            database_form = week_start_dates[0]
            if database_form.week_start == last_monday:
                existing = True  
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = get_initial_data(form6_model, database_form)
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
            finalFacility = options
            
            if A_valid:
                A = data.save(commit=False)
                A.facilityChoice = options
                A.save()

                filled_out = True
                # for items in week_almost.whatever().values():
                #    if items == None:
                #        filled_out = False
                #        break
                if filled_out:
                    createNotification(facility, request, fsID, now, 'submitted', False)
                    updateSubmissionForm(fsID, True, todays_log.date_save)
                else:
                    if formSubmissionRecords_model.objects.filter(formID__id=formName, facilityChoice__facility_name=facility).exists():
                        subForm = formSubmissionRecords_model.objects.filter(formID__id=formName, facilityChoice__facility_name=facility)[0]
                    subForm.submitted = False
                    subForm.save()
            return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    return render(request, "shared/forms/daily/formB.html", {
        'fsID': fsID, 
        'picker': picker, 
        'weather': weather2, 
        "search": search, 
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        "back": back, 
        'todays_log': todays_log, 
        'end_week': end_week, 
        'data': data, 
        'profile': profile, 
        'selector': selector, 
        'formName': formName, 
        'notifs': notifs,
        'freq2': freq2,
        'freq': freq,
        'facility': facility
    })
