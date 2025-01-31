from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime, date
from ..models import daily_battery_profile_model, form27_model, bat_info_model
from ..forms import quarterly_trucks_form
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from ..utils import createNotification, get_initial_data, getFacSettingsInfo, checkIfFacilitySelected, issueForm_picker,updateSubmissionForm, setUnlockClientSupervisor

lock = login_required(login_url='Login')

@lock
def quarterly_trucks(request, facility, fsID, selector):
    formName = 27
    freq = getFacSettingsInfo(fsID)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    existing = False
    search = False
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all().filter(facility_name=facility)[0]
    submitted_forms = form27_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    today = date.today()
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
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date())
            database_model = form_query[0] if form_query.exists() else print('no data found with this date')
            data = database_model
            existing = True
            search = True
            unlock = True
        elif now == todays_log.date_save:
            if submitted_forms.exists():
                database_form = submitted_forms[0]
                if what_quarter(todays_log.date_save) == what_quarter(database_form.date) and todays_log.date_save.year == database_form.date.year:
                    existing = True
        else:
            batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            return redirect('daily_battery_profile', facility, "login", batt_prof_date)
        
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = get_initial_data(form27_model, database_form)
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
                A = data.save(commit=False)
                A.facilityChoice = options
                A.save()
                
                filled_out = True
                for items in A.whatever().values():
                    if items is None or items == '':
                        filled_out = False  # -change this back to false
                        break
                if filled_out:
                    ## if issue found find it here
                    createNotification(facility, request, fsID, now, 'submitted', False)
                    updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
            
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