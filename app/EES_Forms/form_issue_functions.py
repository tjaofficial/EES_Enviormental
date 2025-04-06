from .models import issues_model
from .utils import createNotification, updateSubmissionForm

def call_dynamic_function(form_number, *args, **kwargs):
    if form_number in FUNCTION_MAP:
        return FUNCTION_MAP[form_number](*args, **kwargs)  # ✅ Automatically passes all arguments
    else:
        raise ValueError(f"No function found for form {form_number}")

def form1_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------

    # if A.ovens_data['comments'] not in {'-', 'n/a', 'N/A'}:
    #     issue_page = '../../issues_view/A-1/' + str(database_form.date) + '/form'
    #     return redirect (issue_page)
    sec = {float(savedForm.ovens_data['charge_1']['c1_sec']), float(savedForm.ovens_data['charge_2']['c2_sec']), float(savedForm.ovens_data['charge_3']['c3_sec']), float(savedForm.ovens_data['charge_4']['c4_sec']), float(savedForm.ovens_data['charge_5']['c5_sec'])}
    if float(savedForm.ovens_data['total_seconds']) >= 55:
        issueFound = True
        compliance = True
    else:
        for x in sec:
            if 10 <= x:
                issueFound = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form2_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if savedForm.notes not in {'-', 'n/a', 'N/A'} or savedForm.leaking_doors != 0:
        issueFound = True
        if savedForm.leaking_doors > 8:
            compliance = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form3_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if savedForm.notes not in {'-', 'n/a', 'N/A'} or int(savedForm.om_leaks) > 0 or int(savedForm.l_leaks) > 0: 
        issueFound = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form4_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if savedForm.notes.lower() != 'no ve' or savedForm.leak_data != "{}":
        issueFound = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form5_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if float(savedForm.ovens_data['oven1']['highest_opacity']) >= 10 or float(savedForm.ovens_data['oven1']['average_6_opacity']) >= 35 or savedForm.ovens_data['oven1']['opacity_over_20'] == 'Yes' or savedForm.ovens_data['oven1']['average_6_over_35'] == 'Yes':
        issueFound = True
    elif float(savedForm.ovens_data['oven2']['highest_opacity']) >= 10 or float(savedForm.ovens_data['oven2']['average_6_opacity']) >= 35 or savedForm.ovens_data['oven2']['opacity_over_20'] == 'Yes' or savedForm.ovens_data['oven2']['average_6_over_35'] == 'Yes':
        issueFound = True
    elif float(savedForm.ovens_data['oven3']['highest_opacity']) >= 10 or float(savedForm.ovens_data['oven3']['average_6_opacity']) >= 35 or savedForm.ovens_data['oven3']['opacity_over_20'] == 'Yes' or savedForm.ovens_data['oven3']['average_6_over_35'] == 'Yes':
        issueFound = True
    elif float(savedForm.ovens_data['oven4']['highest_opacity']) >= 10 or float(savedForm.ovens_data['oven4']['average_6_opacity']) >= 35 or savedForm.ovens_data['oven4']['opacity_over_20'] == 'Yes' or savedForm.ovens_data['oven4']['average_6_over_35'] == 'Yes':
        issueFound = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form6_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.week_start, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    filled_out = True
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    # for items in week_almost.whatever().values():
    #    if items == None:
    #        filled_out = False
    #        break
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.week_start), issue_page)
    if filled_out:
        createNotification(facility, request, fsID, form_variables['now'], 'submitted', False)
        updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    else:
        # if formSubmissionRecords_model.objects.filter(formID__id=form_variables['formName'], facilityChoice__facility_name=facility).exists():
        #     subForm = formSubmissionRecords_model.objects.filter(formID__id=form_variables['formName'], facilityChoice__facility_name=facility)[0]
        # subForm.submitted = False
        # subForm.save()
        print("Need something")
    return ('IncompleteForms', facility)

def form7_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    for areaNumb in range(1,5):
        areaJson = getattr(savedForm, f"area_json_{areaNumb}", False)
        if areaJson:
            issueFound = True if areaJson['average'] > 5 else False
              
    issueFound = True if savedForm.comments not in {'-', 'n/a', 'N/A'} else False
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form8_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.week_start, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    new_latest_form = form_variables['submitted_forms'][0]
    filled_out = True
    for items in new_latest_form.whatever().values():
        if items is None or items == '':
            #print("check 4")
            print("not filled out all the way")
            filled_out = False  # -change this back to false
            break
    print(filled_out)
    if filled_out:
        createNotification(facility, request, fsID, form_variables['now'], 'submitted', False)
        updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    else:
        # if formSubmissionRecords_model.objects.filter(formID__id=form_variables['formName'], facilityChoice__facility_name=facility).exists():
        #     subForm = formSubmissionRecords_model.objects.filter(formID__id=form_variables['formName'], facilityChoice__facility_name=facility)[0]
        # subForm.submitted = False
        # subForm.save()
        print("Need to handle")
    return ('IncompleteForms', facility)

def form9_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if savedForm.leaks == "Yes":
        issueFound = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form17_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form18_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form19_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form20_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.week_start, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)

    if savedForm.is_fully_filled():
        createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form21_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.week_start, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if 'Yes' in {savedForm.vents_0, savedForm.mixer_0, savedForm.vents_1, savedForm.mixer_1, savedForm.vents_2, savedForm.mixer_2, savedForm.vents_3, savedForm.mixer_3, savedForm.vents_4, savedForm.mixer_4, savedForm.vents_5, savedForm.mixer_5, savedForm.vents_6, savedForm.mixer_6}:
        return ("form19", facility, fsID, 'formL')
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    
    if savedForm.is_fully_filled():
        createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form24_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if 'Yes' in {savedForm.Q_2,savedForm.Q_3,savedForm.Q_4,savedForm.Q_5,savedForm.Q_6,savedForm.Q_7,savedForm.Q_8,savedForm.Q_9}:
        issueFound = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form25_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    if 'Yes' in {savedForm.Q_2,savedForm.Q_3,savedForm.Q_4,savedForm.Q_5,savedForm.Q_6,savedForm.Q_7,savedForm.Q_8,savedForm.Q_9}:
        issueFound = True
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form26_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    return ('IncompleteForms', facility)

def form27_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    if savedForm.is_fully_filled():
        createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form29_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #--------vvvvvvv INSERT ANY CHECKS HERE vvvvvv----------------
    
    #--------^^^^^^^ INSERT ANY CHECKS HERE ^^^^^^^^----------------
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    if savedForm.is_fully_filled():
        createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form30_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #INSERT ANY CHECKS HERE
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

def form31_issue_check(savedForm, form_variables, request, selector, facility, database_form, fsID, *args, **kwargs):
    fsID = str(fsID)
    finder = issues_model.objects.filter(date=savedForm.date, formChoice=savedForm.formSettings).exists()
    issueFound = False
    compliance = False
    #INSERT ANY CHECKS HERE
    if issueFound:
        if finder:
            if selector == 'form':
                issue_page = 'resubmit'
            else:
                issue_page = 'issue'
        else:
            issue_page = 'form'
        
        if compliance:
            issue_page = issue_page + "-c"
            
        return ('issues_view', facility, fsID, str(database_form.date), issue_page)
    createNotification(facility=facility, request=request, fsID=fsID, date=form_variables['now'], notifSelector='submitted', issueID=False)        
    updateSubmissionForm(fsID, True, form_variables['daily_prof'][0].date_save)
    return ('IncompleteForms', facility)

FUNCTION_MAP = {
    "1": form1_issue_check,
    "2": form2_issue_check,
    "3": form3_issue_check,
    "4": form4_issue_check,
    "5": form5_issue_check,
    "6": form6_issue_check,
    "7": form7_issue_check,
    "8": form8_issue_check,
    "9": form9_issue_check,
    "17": form17_issue_check,
    "18": form18_issue_check,
    "19": form19_issue_check,
    "20": form20_issue_check,
    "21": form21_issue_check,
    "24": form24_issue_check,
    "25": form25_issue_check,
    "26": form26_issue_check,
    "27": form27_issue_check,
    "29": form29_issue_check,
    "30": form30_issue_check,
    "31": form31_issue_check,
}



# def __init__(self, *args, **kwargs):
#     form_settings = kwargs.pop("form_settings", None)

#     if not form_settings:
#         raise ValueError("Error: `form_settings` must be provided when initializing form1_form.")
#     """ Extract JSON values and create dynamic form fields with the correct styles. """
#     super().__init__(*args, **kwargs)