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
            initial_data = database_model
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
                }
                attrList = [
                    'observer',
                    'truck_id',
                    'time',
                    'date',
                    'contents',
                    'freeboard',
                    'wetted',
                    'comments'
                ]
                for i in range(1, 6):
                    for attLabel in attrList:
                        item_value = getattr(database_form, f"{attLabel}{i}")
                        if item_value and item_value != None:
                            if attLabel == 'date':
                                initial_data[attLabel+str(i)] = item_value.strftime("%Y-%m-%d")
                            elif attLabel == 'time':
                                initial_data[attLabel+str(i)] = item_value.strftime("%H:%M")
                            else:
                                initial_data[attLabel+str(i)] = item_value
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
            print("check 1")
            print(request.POST)
            if existing:
                print("check 2")
                form = formD_form(request.POST, instance=database_form)
            else:
                print("check 2.1")
                form = formD_form(request.POST)
            A_valid = form.is_valid()
            if A_valid:
                print("check 3")
                A = form.save(commit=False)
                A.facilityChoice = options
                A.save()
                
                new_latest_form = form8_model.objects.all().order_by('-week_start')[0]
                filled_out = True
                for items in new_latest_form.whatever().values():
                    if items is None or items == '':
                        print("check 4")
                        print("not filled out all the way")
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
