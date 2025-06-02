from datetime import datetime, timedelta
from .models import form_settings_model, daily_battery_profile_model, facility_model
from .utils import checkIfFacilitySelected, getFacSettingsInfo, setUnlockClientSupervisor, issueForm_picker, what_quarter
from .form_issue_functions import call_dynamic_function
from django.apps import apps # type: ignore
from django.shortcuts import redirect # type: ignore
from django.contrib import messages # type: ignore


def initiate_form_variables(fsID, requestUser, selector):
    fsIDSelect = form_settings_model.objects.get(id=int(fsID))
    facility = fsIDSelect.facilityChoice
    facilityName = facility.facility_name
    freq = getFacSettingsInfo(fsID)
    formName = freq.formChoice.form
    notifs = checkIfFacilitySelected(requestUser)
    unlock, client, supervisor = setUnlockClientSupervisor(requestUser)
    now = datetime.now().date()
    print(f'This is the date right now:{now}')
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice=facility).order_by('-date_save')
    options = freq.facilityChoice
    full_name = requestUser.get_full_name()
    picker = issueForm_picker(facilityName, selector, fsID)
    try:
        selectedModel = apps.get_model('EES_Forms', fsIDSelect.formChoice.link + "_model")
        # print(selectedModel.objects.all())
        try:
            submitted_forms = selectedModel.objects.filter(formSettings=fsIDSelect).order_by('-date')
            #print("CHECK submitted forms")
            # print(submitted_forms)
        except:
            submitted_forms = selectedModel.objects.filter(formSettings=fsIDSelect).order_by('-week_start')
    except:
        submitted_forms = False
    
    return dict(locals()) 

def existing_or_new_form(todays_log, selector, submitted_forms, now, facility, request, fsID):
    existing = False
    search = False
    database_form = False
    data = False
    #print(submitted_forms)
    print(selector)
    if selector not in ('form', 'edit'):
        try:
            print(submitted_forms)
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date(), formSettings__id=fsID).order_by('-date')
            print(f"The query filters by date", form_query)
        except:
            selectorDateParsed = datetime.strptime(selector, "%Y-%m-%d").date()
            todays_num = selectorDateParsed.weekday()
            startDate = selectorDateParsed - timedelta(days=todays_num)
            form_query = submitted_forms.filter(week_start=startDate, formSettings__id=fsID).order_by('-week_start')
            print(f"check week", form_query)
        database_model = form_query[0] if form_query.exists() else False
        if database_model:
            data = database_model
            existing = True
            search = True
            print(f"archive and everything is true")
        else:
            messages.error(request,"ERROR: ID-11850005. Contact Support Team.")
            #return sendToDash(request.user)
    elif now == todays_log.date_save:
        if submitted_forms.exists():
            database_form = submitted_forms.filter(formSettings__id=fsID)[0]
            if database_form.formSettings and database_form.formSettings.formChoice.frequency.lower() == "quarterly":
                if what_quarter(todays_log.date_save) == what_quarter(database_form.date) and todays_log.date_save.year == database_form.date.year:
                    existing = True
                    data = database_form
            else:
                print("CHECK 1")
                try:
                    print("CHECK 3")
                    existing = True if todays_log.date_save == database_form.date else False
                    data = database_form if todays_log.date_save == database_form.date else "new_form"
                except:
                    print("CHECK 2")
                    ## this needs to be optimized for a dynamic choice of when the week actually starts
                    ## right now this is optimaized for weekdays or full weeks starting with saturdays
                    ## at the very least it needs to be optimized for if the starting day of the week is Sat-Mon.
                    starting_day = (now - timedelta(days=now.weekday())) if database_form.formSettings.formChoice.day_freq.lower() == "weekdays" else (now - timedelta(days=now.weekday() + 2 if now.weekday() < 5 else (-5 + now.weekday())))
                    print(f"Last monday is: {starting_day}")
                    print(f"the record start date is: {database_form.week_start}")
                    existing = True if starting_day == database_form.week_start else False
                    data = database_form if todays_log.date_save == database_form.week_start else "new_form"
                    print(existing)
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', "login", batt_prof_date)
    
    return data, existing, search, database_form

def template_validate_save(dataFilledForm, form_variables1, *args, **kwargs):
    print(dataFilledForm.errors)
    if dataFilledForm.is_valid():
        A = dataFilledForm.save(commit=False)
        A.formSettings = form_variables1['freq']
        A.save()
        print("checkpoint: end of template_validate_save")
        return call_dynamic_function(
            form_variables1['formName'],  # form number (30, 31, 32)
            A,  # savedForm
            form_variables1,  # form_variables
            *args,  # Pass additional positional arguments
            **kwargs  # Pass keyword arguments
        )
    else:
        return "failed to validate. If no form errors are displayed form is not defined"

    

