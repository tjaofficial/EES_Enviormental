from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
import datetime
from ..models import daily_battery_profile_model, user_profile_model, quarterly_trucks_model, Forms, bat_info_model
from ..forms import quarterly_trucks_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor

lock = login_required(login_url='Login')

@lock
def quarterly_trucks(request, facility, fsID, selector):
    formName = "27"
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    now = datetime.datetime.now().date()
    today = datetime.date.today()
    submitted_forms = quarterly_trucks_model.objects.all().order_by('-date')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    picker = issueForm_picker(facility, selector, fsID)
    
    def what_quarter(input):
        if input.month in {1,2,3}:
            return 1
        if input.month in {4,5,6}:
            return 2
        if input.month in {7,8,9}:
            return 3
        if input.month in {10,11,12}:
            return 4
    
    if daily_prof.exists():
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in submitted_forms:
                if str(x.date) == str(selector):
                    database_model = x
            data = database_model
            existing = True
            search = True
            unlock = True
        elif now == todays_log.date_save.day:
            if submitted_forms.exists():
                database_form = submitted_forms[0]
                if what_quarter(todays_log.date_save) == what_quarter(database_form.date):
                    existing = True
        
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'quarter': database_form.quarter,
                    'date': database_form.date,
                    'observer_5_1': database_form.observer_5_1,
                    'date_5_1': database_form.date_5_1,
                    'time_5_1': database_form.time_5_1,
                    'comments_5_1': database_form.comments_5_1,
                    'rear_gate_5_1': database_form.rear_gate_5_1,
                    'box_interior_5_1': database_form.box_interior_5_1,
                    'box_exterior_5_1': database_form.box_exterior_5_1,
                    'exhaust_5_1': database_form.exhaust_5_1,
                    'observer_6_2': database_form.observer_6_2,
                    'date_6_2': database_form.date_6_2,
                    'time_6_2': database_form.time_6_2,
                    'comments_6_2': database_form.comments_6_2,
                    'rear_gate_6_2': database_form.rear_gate_6_2,
                    'box_interior_6_2': database_form.box_interior_6_2,
                    'box_exterior_6_2': database_form.box_exterior_6_2,
                    'exhaust_6_2': database_form.exhaust_6_2,
                    'observer_7_3': database_form.observer_7_3,
                    'date_7_3': database_form.date_7_3,
                    'time_7_3': database_form.time_7_3,
                    'comments_7_3': database_form.comments_7_3,
                    'rear_gate_7_3': database_form.rear_gate_7_3,
                    'box_interior_7_3': database_form.box_interior_7_3,
                    'box_exterior_7_3': database_form.box_exterior_7_3,
                    'exhaust_7_3': database_form.exhaust_7_3,
                    'observer_9_4': database_form.observer_9_4,
                    'date_9_4': database_form.date_9_4,
                    'time_9_4': database_form.time_9_4,
                    'comments_9_4': database_form.comments_9_4,
                    'rear_gate_9_4': database_form.rear_gate_9_4,
                    'box_interior_9_4': database_form.box_interior_9_4,
                    'box_exterior_9_4': database_form.box_exterior_9_4,
                    'exhaust_9_4': database_form.exhaust_9_4,
                }
            else:
                initial_data = {
                    'quarter': what_quarter(today),
                    'date': today,
                }
            data = quarterly_trucks_form(initial=initial_data)
            
            
        if request.method == "POST":
            if existing:
                data = quarterly_trucks_form(request.POST, instance=database_form)
            else:
                data = quarterly_trucks_form(request.POST)
            A_valid = data.is_valid()
            print(data.errors)
            if A_valid:
                data.save(commit=False)
                data.facilityChoice = options
                data.save()
                
                new_latest_form = quarterly_trucks_model.objects.all().order_by('-date')[0]
                filled_out = True
                for items in new_latest_form.whatever().values():
                    if items is None or items == '':
                        filled_out = False  # -change this back to false
                        break
                if filled_out:
                    updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)
            
    return render(request, "shared/forms/quarterly/quarterly_trucks.html", {
        'picker': picker, 
        'facility': facility, 
        'notifs': notifs,
        'freq': freq,
        "search": search, 
        "client": client, 
        'unlock': unlock, 
        'supervisor': supervisor, 
        'formName': formName, 
        'selector': selector, 
        'data': data
    })