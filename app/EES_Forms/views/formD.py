from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, form8_model, bat_info_model, formSubmissionRecords_model
from ..forms import formD_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import checkIfFacilitySelected, issueForm_picker, getFacSettingsInfo, updateSubmissionForm, setUnlockClientSupervisor, createNotification

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')

@lock
def formD(request, facility, fsID, selector):
    formName = 8
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    today = datetime.date.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_saturday + one_week
    sunday = today - datetime.timedelta(days=1)
    submitted_forms = form8_model.objects.all().order_by('-week_start')
    picker = issueForm_picker(facility, selector, fsID)
    
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in submitted_forms:
                if str(x.week_start) == str(selector):
                    database_model = x
            form = database_model
            existing = True
            search = True
            unlock = True
        elif submitted_forms.exists():
            database_form = submitted_forms[0]
            #print(database_form.whatever().values())
            starting_saturday = database_form.week_start
            if today.weekday() not in {5, 6}:
                if starting_saturday == last_saturday:
                    existing = True
            elif today.weekday() == 5:
                if starting_saturday == today:
                    existing = True
            elif starting_saturday == sunday:
                existing = True
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'week_start': database_form.week_start,
                    'week_end': database_form.week_end,
                    'truck_id1': database_form.truck_id1,
                    'date1': database_form.date1.strftime("%Y-%m-%d") if database_form.date1 else database_form.date1,
                    'time1': database_form.time1.strftime("%H:%M") if database_form.time1 else database_form.time1,
                    'contents1': database_form.contents1,
                    'freeboard1': database_form.freeboard1,
                    'wetted1': database_form.wetted1,
                    'comments1': database_form.comments1,
                    'truck_id2': database_form.truck_id2,
                    'date2': database_form.date2.strftime("%Y-%m-%d") if database_form.date2 else database_form.date2,
                    'time2': database_form.time2.strftime("%H:%M") if database_form.time2 else database_form.time2,
                    'contents2': database_form.contents2,
                    'freeboard2': database_form.freeboard2,
                    'wetted2': database_form.wetted2,
                    'comments2': database_form.comments2,
                    'truck_id3': database_form.truck_id3,
                    'date3': database_form.date3.strftime("%Y-%m-%d") if database_form.date3 else database_form.date3,
                    'time3': database_form.time3.strftime("%H:%M") if database_form.time3 else database_form.time3,
                    'contents3': database_form.contents3,
                    'freeboard3': database_form.freeboard3,
                    'wetted3': database_form.wetted3,
                    'comments3': database_form.comments3,
                    'truck_id4': database_form.truck_id4,
                    'date4': database_form.date4.strftime("%Y-%m-%d") if database_form.date4 else database_form.date4,
                    'time4': database_form.time4.strftime("%H:%M") if database_form.time4 else database_form.time4,
                    'contents4': database_form.contents4,
                    'freeboard4': database_form.freeboard4,
                    'wetted4': database_form.wetted4,
                    'comments4': database_form.comments4,
                    'truck_id5': database_form.truck_id5,
                    'date5': database_form.date5.strftime("%Y-%m-%d") if database_form.date5 else database_form.date5,
                    'time5': database_form.time5.strftime("%H:%M") if database_form.time5 else database_form.time5,
                    'contents5': database_form.contents5,
                    'freeboard5': database_form.freeboard5,
                    'wetted5': database_form.wetted5,
                    'comments5': database_form.comments5,
                    'observer1': database_form.observer1,
                    'observer2': database_form.observer2,
                    'observer3': database_form.observer3,
                    'observer4': database_form.observer4,
                    'observer5': database_form.observer5
                }
            else:
                if today.weekday() == 5:
                    initial_data = {
                        'week_start': today,
                        'week_end': today + datetime.timedelta(days=6)
                    }
                elif today.weekday() == 6:
                    initial_data = {
                        'week_start': today - datetime.timedelta(days=1),
                        'week_end': today + datetime.timedelta(days=5)
                    }
                else:
                    initial_data = {
                        'week_start': last_saturday,
                        'week_end': end_week
                    }
            form = formD_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formD_form(request.POST, instance=database_form)
            else:
                form = formD_form(request.POST)
            A_valid = form.is_valid()
            if A_valid:
                A = form.save(commit=False)
                A.facilityChoice = options
                A.save()
                
                new_latest_form = form8_model.objects.all().order_by('-week_start')[0]
                filled_out = True
                for items in new_latest_form.whatever().values():
                    if items is None or items == '':
                        filled_out = False  # -change this back to false
                        break
                print(filled_out)
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
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "shared/forms/weekly/formD.html", {
        'fsID': fsID, 
        'picker': picker, 
        "search": search, 
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        'form': form, 
        "back": back, 
        'todays_log': todays_log, 
        'profile': profile, 
        'selector': selector, 
        'formName': formName, 
        'facility': facility,
        'notifs': notifs,
        'freq': freq,
        'amountOfTrucks': [1,2,3,4,5],
        'initial_data': initial_data
    })
