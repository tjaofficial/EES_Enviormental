from datetime import datetime, timedelta
from .models import form_settings_model, daily_battery_profile_model, bat_info_model
from .utils import checkIfFacilitySelected, getFacSettingsInfo, setUnlockClientSupervisor, issueForm_picker, what_quarter
from .form_issue_functions import call_dynamic_function
from django.apps import apps # type: ignore
from django.shortcuts import redirect # type: ignore
from django.contrib import messages # type: ignore


def initiate_form_variables(fsID, requestUser, facility, selector):
    freq = getFacSettingsInfo(fsID)
    formName = freq.formChoice.form
    notifs = checkIfFacilitySelected(requestUser, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(requestUser)
    now = datetime.now().date()
    daily_prof = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.filter(facility_name=facility)[0]
    full_name = requestUser.get_full_name()
    picker = issueForm_picker(facility, selector, fsID)
    fsIDSelect = form_settings_model.objects.get(id=int(fsID))
    try:
        selectedModel = apps.get_model('EES_Forms', freq.formChoice.link + "_model")
        #print(selectedModel.objects.all())
        try:
            submitted_forms = selectedModel.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-date')
            #print("CHECK submitted forms")
            print(submitted_forms)
        except:
            submitted_forms = selectedModel.objects.filter(formSettings__facilityChoice__facility_name=facility).order_by('-week_start')
    except:
        submitted_forms = False
    
    return dict(locals()) 

def existing_or_new_form(todays_log, selector, submitted_forms, now, facility, request):
    existing = False
    search = False
    database_form = False
    data = False

    if selector not in ('form', 'edit'):
        try:
            form_query = submitted_forms.filter(date=datetime.strptime(selector, "%Y-%m-%d").date()).order_by('-date')
            print("check date")
        except:
            form_query = submitted_forms.filter(week_start=datetime.strptime(selector, "%Y-%m-%d").date()).order_by('-week_start')
            print("check week")
        database_model = form_query[0] if form_query.exists() else False
        if database_model:
            data = database_model
            existing = True
            search = True
        else:
            messages.error(request,"ERROR: ID-11850002. Contact Support Team.")
            #return sendToDash(request.user)
    elif now == todays_log.date_save:
        print("check 2")
        if submitted_forms.exists():
            print("check 3")
            database_form = submitted_forms[0]
            if database_form.formSettings and database_form.formSettings.formChoice.frequency.lower() == "quarterly":
                if what_quarter(todays_log.date_save) == what_quarter(database_form.date) and todays_log.date_save.year == database_form.date.year:
                    existing = True
                    data = database_form
            else:
                try:
                    existing = True if todays_log.date_save == database_form.date else False
                    data = database_form if todays_log.date_save == database_form.date else "new_form"
                except:
                    starting_monday = now - timedelta(days=now.weekday())
                    existing = True if starting_monday == database_form.week_start else False
                    data = database_form if todays_log.date_save == database_form.week_start else "new_form"
    else:
        batt_prof_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        return redirect('daily_battery_profile', facility, "login", batt_prof_date)
    
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

    

