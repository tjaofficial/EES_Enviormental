from django.shortcuts import render, redirect
from ..models import user_profile_model, issues_model, Forms, Event, daily_battery_profile_model, User, sop_model, formA1_readings_model, formA2_model, formA3_model, formA4_model, formA5_readings_model, bat_info_model, formM_model, facility_forms_model, formSubmissionRecords_model, User
from ..forms import issues_form, events_form, sop_form
import datetime
import calendar
from django.core.exceptions import FieldError
from django.db.models import Q
from django.apps import apps
from ..utils import Calendar, updateSubmissionForm, setUnlockClientSupervisor, colorModeSwitch, checkIfFacilitySelected, getCompanyFacilities, getFormID_w_newFormLabel
from django.contrib.auth.decorators import login_required
import os
import ast
from django.contrib import messages
from django.conf import settings
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from .print_form_view import date_change
lock = login_required(login_url='Login')


@lock
def corrective_action_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    
    issueForm_query = request.GET.get('issueForm')
    issueMonth_query = request.GET.get('issueMonth')
    issueDate_query = request.GET.get('issueDate')
    issue_contains_query = request.GET.get('issue_contains')
    notified_query = request.GET.get('notified')
    ca_forms = issues_model.objects.all().filter(facilityChoice__facility_name=facility).order_by('-id')
    
    varPull = [
        issueForm_query,
        issueMonth_query,
        issueDate_query,
        issue_contains_query,
        notified_query
    ]

    def issueFormFunc(issueForm_query, ca_forms):
        if issueForm_query != "" and issueForm_query is not None:
            #print("Pre-Form-Search")
            #print(ca_forms)
            ca_forms = ca_forms.filter(form__icontains=issueForm_query)
            #print("Post-Form-Search")
            #print(ca_forms)
            return ca_forms
        else:
            return "none"
    
    def issueMonthFunc(issueMonth_query, ca_forms):
        if issueMonth_query != "" and issueMonth_query is not None:
            #print("Pre-Month-Search")
            #print(ca_forms)
            issueMonth_query = datetime.datetime.strptime(issueMonth_query, "%Y-%m").date()
            ca_forms = ca_forms.filter(date__month=issueMonth_query.month, date__year=issueMonth_query.year)
            #print("Post-Month-Search")
            #print(ca_forms)
            return ca_forms
        else:
            return "none"
    
    def issueDateFunc(issueDate_query, ca_forms):
        if issueDate_query != "" and issueDate_query is not None:
            issueDate_query = datetime.datetime.strptime(issueDate_query, "%Y-%m-%d").date()
            ca_forms = ca_forms.filter(date__year=issueDate_query.year, date__month=issueDate_query.month, date__day=issueDate_query.day)
            return ca_forms
        else:
            return "none"
    
    def issue_containsFunc(issue_contains_query, ca_forms):
        if issue_contains_query != "" and issue_contains_query is not None:
            ca_forms = ca_forms.filter(issues__icontains=issue_contains_query)
            return ca_forms
        else:
            return "none"
    
    def notifiedfunc(notified_query, ca_forms):
        if notified_query != "" and notified_query is not None:
            #print("Pre-Notified-Search")
            #print(ca_forms)
            ca_forms = ca_forms.filter(notified__icontains=notified_query)
            #print("Post-Notified-Search")
            #print(ca_forms)
            return ca_forms
        else:
            return "none"
    
    searchList = [
        issueFormFunc(issueForm_query, ca_forms),
        issueMonthFunc(issueMonth_query, ca_forms),
        issueDateFunc(issueDate_query, ca_forms),
        issue_containsFunc(issue_contains_query, ca_forms),
        notifiedfunc(notified_query, ca_forms)
    ]
    
    filterReturn = []
    notEmpty = False
    inputsUsedCount = 0
    for x in searchList:
        if x != 'none':
            inputsUsedCount += 1
            for y in x:
                filterReturn.append(y)
            notEmpty = True
    #print(filterReturn)

    unisonResults = []
    usedItems = []
    for i in range(len(filterReturn)):
        result = filterReturn[i]
        count = 0
        #print("<------USE")
        #print(i)
        if result not in usedItems:
            for z in range(len(filterReturn)):
                result2 = filterReturn[z]
                #print("<------Compared")
                #print(z)
                if result == result2:
                    count += 1
                    #print("<---------------------COUNT")
                    if count == inputsUsedCount:
                        if result2 not in unisonResults:
                            unisonResults.append(result2)
                            #print("Adding " + str(result2) + " to the unison list")
            #print("------END LOOP-------")
            usedItems.append(result)
        else:
            #print("------END LOOP-------")
            continue
    
    #print(unisonResults)
    if notEmpty:
        if unisonResults:
            ca_forms = unisonResults
        else:
            ca_forms = "empty"
    
    profile = user_profile_model.objects.all()
    options = bat_info_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if answer['facilitySelect'] != '':
            return redirect('Corrective-Action', answer['facilitySelect'])
    return render(request, "shared/corrective_actions.html", {
        'notifs': notifs, "varPull": varPull, 'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'ca_forms': ca_forms, 'profile': profile, 'client': client, "supervisor": supervisor, "unlock": unlock, 
    })

@lock
def calendar_view(request, facility, year, month):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    options = bat_info_model.objects.all()
    profile = user_profile_model.objects.all()
    try:
        month_number = int(month)
        month = calendar.month_name[month_number]
    except:
        month = month.title()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)
        

    if month_number == 1:
        prev_month = str(calendar.month_name[12])
        prev_year = str(year - 1)
    else:
        prev_month = str(calendar.month_name[month_number - 1])
        prev_year = year

    if month_number == 12:
        next_month = str(calendar.month_name[1])
        next_year = str(year + 1)
    else:
        next_month = str(calendar.month_name[month_number + 1])
        next_year = year

    events = Event.objects.all()

    calend = Calendar()
    calend.setfirstweekday(6)
    html_cal = calend.formatmonth(year, month_number, year, facility, withyear=True)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard', answer['facilitySelect'])
    return render(request, "ees_forms/schedule.html", {
        'notifs': notifs, 'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, "supervisor": supervisor, 'year': year, 'month': month, 'prev_month': prev_month, 'next_month': next_month, 'events': events, 'html_cal': html_cal, 'prev_year': prev_year, 'next_year': next_year, 'profile': profile, 'unlock': unlock, 'client': client,
    })

@lock
def schedule_view(request, facility):
    supervisor = False
    options = bat_info_model.objects.all()
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    today_year = int(datetime.date.today().year)
    today_month = str(calendar.month_name[datetime.date.today().month])

    return redirect('schedule/' + str(today_year) + '/' + str(today_month))

    return render(request, "ees_forms/scheduling.html", {
        'options': options, 'facility': facility, 'today_year': today_year, 'today_month': today_month, 'supervisor': supervisor,
    })

@lock
def archive_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    options = bat_info_model.objects.all()
    profile = user_profile_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if request.method == 'POST':
        answer = request.POST
        if supervisor:
            if answer['facilitySelect'] != '':
                return redirect('archive', answer['facilitySelect'])
        else:
            if 'colorMode' in answer.keys():
                colorModeSwitch(request)

    return render(request, 'shared/archive.html', {
        'notifs': notifs, 'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'profile': profile, 'client': client, "supervisor": supervisor, "unlock": unlock, 
    })

@lock
def search_forms_view(request, facility, access_page):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    readingsData = False
    ModelForms = Forms.objects.all()
    weekend = False
    monthList =''
    options = bat_info_model.objects.all()
    profile = user_profile_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    facilitiesForm = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
    formSubs = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    if facilitiesForm.exists():
        formIDandLabel = ast.literal_eval(facilitiesForm[0].formData)
    if access_page != 'search':
        if access_page != 'formN_model':
            chk_database = apps.get_model('EES_Forms', access_page).objects.count()
            print(apps.get_model('EES_Forms', access_page).objects.all())
            mainList = []
            # DATE - DAILY = 1, href="../Daily/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.date.year }}-{% if x.date.month < 10 %}0{{x.date.month}}{%else%}{{x.date.month}}{% endif %}-{% if x.date.day < 10 %}0{{x.date.day}}{%else%}{{x.date.day}}{% endif %}"
            # DATE - WEEKLY = 4, href="../Weekly/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.date.year }}-{% if x.date.month < 10 %}0{{x.date.month}}{%else%}{{x.date.month}}{% endif %}-{% if x.date.day < 10 %}0{{x.date.day}}{%else%}{{x.date.day}}{% endif %}{% if weekend %}/{% if x.weekend_day == 5 %}Saturday{% else %}Sunday{% endif %}{% else %}{% endif %}"
            # WEEK - DAILY = 3, href="../Daily/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.week_start.year }}-{% if x.week_start.month < 10 %}0{{x.week_start.month}}{%else%}{{x.week_start.month}}{% endif %}-{% if x.week_start.day < 10 %}0{{x.week_start.day}}{%else%}{{x.week_start.day}}{% endif %}"
            # WEEK - WEEKLY = 2, href="../Weekly/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.week_start.year }}-{% if x.week_start.month < 10 %}0{{x.week_start.month}}{%else%}{{x.week_start.month}}{% endif %}-{% if x.week_start.day < 10 %}0{{x.week_start.day}}{%else%}{{x.week_start.day}}{% endif %}"
            if chk_database == 0:
                att_check = 5
                database = ''
            else:
                try:
                    # THESE ARE FORMS USING DATE
                    database = apps.get_model('EES_Forms', access_page).objects.all().filter(facilityChoice__facility_name=facility).order_by('-date')
                    print('BY DATE')
                    print(database.count())
                    if database.count() == 0:
                        att_check = 5
                        database = ''
                    else:
                        for x in ModelForms:
                            print('CHECK 1')
                            if x.form == access_page[4] or x.form == access_page[4] + '-' + access_page[5] or x.form == access_page[0:-6].replace('_', ' ').title():
                                print(access_page)
                                if x.frequency[0] == 'W':
                                    # THESE ARE WEEKLY FORMS
                                    att_check = 4
                                    if x.weekend_only:
                                        weekend = True
                                    else:
                                        weekend = False
                                elif x.frequency[0] == 'M':
                                    att_check = 6
                                elif x.frequency[0] == 'Q':
                                    att_check = 7
                                else:
                                    # THESE ARE DAILY FORMS
                                    att_check = 1
                            else:
                                print('no match')
                except FieldError as e:
                    # THESE ARE FORMS USING WEEK
                    database = apps.get_model('EES_Forms', access_page).objects.all().filter(facilityChoice__facility_name=facility).order_by('-week_start')
                    print('BY WEEK START')
                    print(database.count())
                    if database.count() == 0:
                        att_check = 5
                        database = ''
                    else:
                        for x in ModelForms:
                            print(x)
                            if x.form == access_page[4] or x.form == access_page[4] + '-' + access_page[5]:
                                # FORMS THAT ARE SINGLE DIDGITS
                                print('it does)')
                                if x.frequency[0] == 'D':
                                    # THESE ARE DAILY FORMS
                                    att_check = 3
                                else:
                                    # THESE ARE WEEKLY FORMS
                                    att_check = 2
                            else:
                                print('Error - EES_00006')
                print(att_check)
                if att_check == 1:
                    for x in database:
                        mainList.append([access_page, x.date, x, 'Daily'])
                elif att_check == 2:
                    for x in database:
                        mainList.append([access_page, x.week_start, x, 'Weekly'])
                elif att_check == 3:
                    for x in database:
                        mainList.append([access_page, x.week_start, x, 'Daily'])
                elif att_check == 4:
                    if not weekend:
                        for x in database:
                            mainList.append([access_page, x.date, x, 'Weekly'])
                    else:
                        for x in database:
                            mainList.append([access_page, x.date, x, 'Weekly', '/' + x.weekend_day])
                elif att_check == 6:
                    for x in database:
                        mainList.append([access_page, x.date, x, 'Monthly'])
                elif att_check == 7:
                    for x in database:
                        mainList.append([access_page, x.date, x, 'Quarterly'])
                        
                        
                try:
                    Model2 = apps.get_model('EES_Forms', access_page[0:7] + 'readings_model')
                    readingsData = True
                    if len(Model2.objects.all()) > 0:
                        database2 = Model2.objects.all().filter(form__facilityChoice__facility_name=facility).order_by('-form')
                    else:
                        database2 = 'empty'
                except LookupError:
                    try:
                        Model2 = apps.get_model('EES_Forms', access_page[0:6] + 'readings_model')
                        readingsData = True
                        if len(Model2.objects.all()) > 0:
                            database2 = Model2.objects.all().filter(form__facilityChoice__facility_name=facility).order_by('-form')
                        else:
                            database2 = 'empty'
                    except LookupError:
                        readingsData = False
                        database2 = ''
        else:
            mainList=''
            database=''
            database2=''
            att_check=''
            queryN = formM_model.objects.all().filter(facilityChoice__facility_name=facility)
            monthList = []
            eliminator =[]
            for month in queryN:
                if month.date.month not in eliminator:
                    monthList.append((month.date.month, month.date.year, calendar.month_name[month.date.month],))
                    eliminator.append(month.date.month)
            print(monthList)

    if request.method == "POST":
        passedData = request.POST
        if 'searched' in passedData.keys():
            searchedText = passedData['searched']
        else:
            searchedText = False
        database = ''
        database2 = ''
        att_check = ''
        mainList = ''
        weekend = False
        
        
        if searchedText:
            form_list = formSubs.filter(Q(formID__form__icontains=searchedText) | Q(formID__frequency__icontains=searchedText) | Q(formID__title__icontains=searchedText)).order_by('formID')
            forms = []
            for subInfo in form_list:
                for facilityForms in formIDandLabel:
                    if subInfo.formID.id == facilityForms[0]: 
                        forms.append((facilityForms, subInfo))
            # forms = form_list
            letterForms = []

            for x in forms:
                if x[0][0] not in {26,27}:
                    letterForms.append([x[0][1], 'form' + x[1].formID.form.replace('-','') + '_model', x[1].formID])
                else:
                    letterForms.append([x[0][1], x[1].formID.form.replace(' ', '_').lower() + '_model', x[1].formID])
            print(letterForms)
        else:
            messages.error(request,"Please enter a form 'Name' or 'Label' to search.")
            return redirect('archive', facility)
            
        return render(request, 'shared/search_forms.html', {
            'notifs': notifs, 
            'sortedFacilityData': sortedFacilityData, 
            'options': options, 
            'facility': facility, 
            'unlock': unlock, 
            'supervisor': supervisor, 
            'letterForms': letterForms, 
            'mainList': mainList, 
            'readingsData': readingsData, 
            'profile': profile, 
            'searched': searchedText, 
            'forms': forms, 
            'access_page': access_page, 
            'database': database, 
            'database2': database2, 
            'att_check': att_check, 
            'weekend': weekend, 
            'client': client,
        })
    else:
        return render(request, 'shared/search_forms.html', {
            'notifs': notifs, 
            'sortedFacilityData': sortedFacilityData, 
            'monthList': monthList, 
            'options': options, 
            'facility': facility, 
            'unlock': unlock, 
            'supervisor': supervisor, 
            'mainList': mainList, 
            'readingsData': readingsData, 
            'profile': profile, 
            'access_page': access_page, 
            'database': database, 
            'database2': database2, 
            'att_check': att_check, 
            'weekend': weekend, 
            'client': client,
        })

@lock
def issues_view(request, facility, form_name, form_date, access_page):
    print(form_name)
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    profile = user_profile_model.objects.all()
    todays_log = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = bat_info_model.objects.all()
    issueModel = issues_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    sortedFacilityData = getCompanyFacilities(request.user.username)

    if todays_log.exists():
        todays_log = todays_log[0]
    if facility_forms_model.objects.filter(facilityChoice__facility_name=facility).exists():
        facilityForms = ast.literal_eval(facility_forms_model.objects.filter(facilityChoice__facility_name=facility)[0].formData)
    if formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility).exists():
        facilitySubs = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    try: 
        form_name = int(form_name)
        form_name_parsed = form_name
    except:
        form_name_parsed = getFormID_w_newFormLabel(form_name, facilityForms)
        if not form_name_parsed:
            messages.error(request,'ERROR: ID-11850001. Contant Support Team')
    
    def create_link_elements():
        for facForms in facilityForms:
            formIDtemp = int(facForms[0])
            for facSubs in facilitySubs:
                if formIDtemp == facSubs.formID.id and formIDtemp == form_name_parsed:
                    formLabel = facForms[1]
                    formID = int(facForms[0])
                    main_url = facSubs.formID.frequency + '/' + facSubs.formID.link + '/'
                    if facSubs.formID.id in {24,25}:
                        weekendNameDict = {5:'saturday', 6: 'sunday'}
                        today = datetime.date.today().weekday()
                        for dayNumber in weekendNameDict:
                            if today == dayNumber:
                                day = weekendNameDict[dayNumber]
                    else:
                        day = False
                    return main_url, day, formLabel, formID

    if access_page == 'form':
        main_url, day, formLabel, formID = create_link_elements()
        if day:
            link = main_url + access_page + '/' + day
        else:
            link = main_url + access_page
        existing = False
        picker = 'n/a'
        
        if issueModel.exists():
            database_form = issueModel[0]
            if todays_log.date_save == database_form.date:
                if database_form.form == formLabel:
                    existing = True
        if existing:
            initial_data = {
                'form': database_form.form,
                'issues': database_form.issues,
                'notified': database_form.notified,
                'time': database_form.time,
                'date': database_form.date,
                'cor_action': database_form.cor_action
            }
        else:             
            initial_data = {
                'date': todays_log.date_save,
                'form': formLabel
            }
            picker = ''
        form = issues_form(initial=initial_data)
        
        if request.method == "POST":
            dataCopy = request.POST.copy()
            dataCopy["facilityChoice"] = options.filter(facility_name=facility)[0]
            if existing:
                data = issues_form(dataCopy, instance=database_form)
            else:
                data = issues_form(dataCopy)
            if data.is_valid():
                data.save()

                updateSubmissionForm(facility, formID, True, todays_log.date_save)

                return redirect('IncompleteForms', facility)
    elif access_page == 'issue':
        main_url, day, formLabel, formID = create_link_elements()
        if day:
            link = main_url + form_date + '/' + day
        else:
            link = main_url + form_date
        org = issues_model.objects.filter(date__exact=form_date)
        database_form = org[0]
        for entry in org:
            if datetime.datetime.strptime(form_date, '%Y-%m-%d').date() == entry.date:
                if form_name == entry.form:
                    picker = entry
                    form = issues_form()
                    if client:
                        entry.viewed = True
                        entry.save()
    elif access_page == 'edit' or access_page == 'resubmit':
        org = issues_model.objects.all().order_by('-date')
        database_form = org[0]
        for entry in org:
            if datetime.datetime.strptime(form_date, '%Y-%m-%d').date() == entry.date:
                if form_name == entry.form:
                    picker = entry
                    link = ''
        initial_data = {
            'form': picker.form,
            'issues': picker.issues,
            'notified': picker.notified,
            'time': picker.time,
            'date': picker.date,
            'cor_action': picker.cor_action
        }

        form = issues_form(initial=initial_data)

        if request.method == "POST":
            dataCopy = request.POST.copy()
            dataCopy["facilityChoice"] = options.filter(facility_name=facility)[0]
            data = issues_form(dataCopy, instance=picker)
            if data.is_valid():
                data.save()
                
                if access_page == 'resubmit':
                    updateSubmissionForm(facility, formID, True, picker.date)
                    
                    return redirect('IncompleteForms', facility)
                else:
                    return redirect('../../../issues_view/' + form_name + '/' + form_date + '/issue')
    else:
        existing = False
        picker = 'n/a'
        if issues_model.objects.count() != 0:
            org = issues_model.objects.all().order_by('-date')
            database_form = org[0]
            if todays_log.date_save == database_form.date:
                if database_form.form == form_name:
                    existing = True
        if existing:
            initial_data = {
                'form': database_form.form,
                'issues': database_form.issues,
                'notified': database_form.notified,
                'time': database_form.time,
                'date': database_form.date,
                'cor_action': database_form.cor_action
            }
        else:
            initial_data = {
                'date': todays_log.date_save,
                'form': form_name
            }

        form = issues_form(initial=initial_data)

        if request.method == "POST":
            dataCopy = request.POST.copy()
            dataCopy["facilityChoice"] = options.filter(facility_name=facility)[0]
            if existing:
                data = issues_form(dataCopy, instance=database_form)
            else:
                data = issues_form(dataCopy)
            if data.is_valid():
                data.save()

                updateSubmissionForm(facility, formID, True, todays_log.date_save)

                return redirect('IncompleteForms', facility)
    return render(request, "shared/issues_template.html", {
        'notifs': notifs, 'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'form': form, 'access_page': access_page, 'picker': picker, "form_date": form_date, 'link': link, 'profile': profile, "unlock": unlock, "client": client, "supervisor": supervisor
    })

@lock
def event_add_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    options = bat_info_model.objects.all()
    companyData = user_profile_model.objects.get(user__id=request.user.id).company
    listOfObservers = user_profile_model.objects.filter(company__id=companyData.id, position='observer')
    
    if options.filter(facility_name=facility).exists():
        finalFacility = options.filter(facility_name=facility)[0]
    else:
        print("MT")
    today = datetime.date.today()
    profile = user_profile_model.objects.all()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    sortedFacilityData = getCompanyFacilities(request.user.username)
    form_var = events_form()
    fullName = request.user.first_name + " " + request.user.last_name

    if request.method == "POST":
        answer = request.POST
        for x in answer:
            if x == 'facilitySelect':
                return redirect('sup_dashboard', answer['facilitySelect'])
        request_form = events_form(request.POST)
        if request_form.is_valid():
            A = request_form.save(commit=False)
            A.enteredBy = fullName
            if facility == "supervisor":
                A.personal = True
            else:
                A.facilityChoice = finalFacility
                A.personal = False
            A.save()

            cal_link = 'schedule/' + str(today_year) + '/' + today_month

            return redirect(cal_link)

    return render(request, "supervisor/event_add.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData,'options': options, 
        'facility': facility, 
        'today_year': today_year, 
        'today_month': today_month, 
        'form': form_var, 
        'profile': profile, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'listOfObservers': listOfObservers
    })

@lock
def event_detail_view(request, facility, access_page, event_id):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    today = datetime.date.today()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    options = bat_info_model.objects.all()
    companyData = user_profile_model.objects.get(user__id=request.user.id).company
    listOfObservers = user_profile_model.objects.filter(company__id=companyData.id, position='observer')
    
    context = {}
    if supervisor:
        context['parent_template'] = 'admin/sup_layout.html'
    else:
        context['parent_template'] = 'ees_forms/layout.html'

    form = events_form()
    if access_page == 'view':
        my_event = Event.objects.get(pk=event_id)
        if request.method == 'POST':
            if "delete" in request.POST.keys():
                data_pull = Event.objects.get(pk=event_id)
                data_pull.delete()
                cal_link = '../../schedule/' + str(today_year) + '/' + today_month
                return redirect(cal_link)
    elif access_page == 'edit':
        data_pull = Event.objects.get(pk=event_id)
        initial_data = {
            'title': data_pull.title,
            'date': data_pull.date,
            'start_time': data_pull.start_time,
            'end_time': data_pull.end_time,
            'notes': data_pull.notes,
        }
        if facility != "supervisor":
            initial_data['observer'] = data_pull.observer
            
        my_event = events_form(initial=initial_data)

        if request.method == 'POST':
            print(request.POST)
            data = events_form(request.POST, instance=data_pull)
            print(data)
            print('pork')
            print(data.errors)
            if data.is_valid():
                A = data.save(commit=False)
                A.enteredBy = request.user.last_name
                if facility == "supervisor":
                    A.personal = True
                print('chicken')
                A.save()

                #return redirect('../../event_detail/' + str(event_id) + '/view')

    
    return render(request, "shared/event_detail.html", {
        'notifs': notifs, 
        'options': options, 
        'facility': facility, 
        'context': context, 
        "supervisor": supervisor, 
        "unlock": unlock, 
        "client": client, 
        'today_year': today_year, 
        'today_month': today_month, 
        'form': form, 
        'my_event': my_event, 
        'event_id': event_id, 
        'access_page': access_page,
        'listOfObservers': listOfObservers
    })

def handlePhone(number):
    number = number[2:]
    first = number[:3]
    middle = number[3:6]
    end = number[6:]
    parsedNumber = '(' + first +')'+ middle + '-' + end
    return parsedNumber
    
@lock
def shared_contacts_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    options = bat_info_model.objects.all()
    companyOfUser = user_profile_model.objects.get(user=request.user).company
    sortedFacilityData = getCompanyFacilities(request.user.username)
    
    companyProfiles = user_profile_model.objects.filter(company=companyOfUser).order_by('user')
    userProfile = companyProfiles.get(user__id=request.user.id)
    
    organized_list = []
    for index, user in enumerate(companyProfiles):
        if user.certs:
            certList = user.certs.split(',')
            i = 0
            for item in certList:
                certList[i] = certList[i].strip()
                i += 1
            organized_list.append((user.id, user, certList, handlePhone(user.phone)))
        else:
            organized_list.append((user.id, user, 'N/A' , handlePhone(user.phone)))
    
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard', answer['facilitySelect'])
    return render(request, "shared/contacts.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        'facility': facility, 
        'userProfile': userProfile, 
        'organized_list': organized_list, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock
    })
    
@lock
def sop_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    sortedFacilityData = getCompanyFacilities(request.user.username)
    options = bat_info_model.objects.all()
    sops = sop_model.objects.all().order_by('name')
    sopForm = sop_form()
    
    if request.method == 'POST':
        form = sop_form(request.POST, request.FILES)
        if form.is_valid():
            A = form.save(commit=False)
            A.pdf_url = A.pdf_file.url
            A.save()
    return render(request, 'shared/sops.html', {
        'sortedFacilityData':sortedFacilityData, 'notifs': notifs, 'options': options, 'facility': facility, 'sops': sops, 'sopForm': sopForm, 'supervisor': supervisor, "client": client, 'unlock': unlock
    })
    
def formsProgress(request, facility, section):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if unlock:
        return redirect('IncompleteForms', facility)
    existsing = False
        
    allForms = Forms.objects.all().order_by('form')
    clientForms = facility_forms_model.objects.filter(facilityChoice__facility_name=facility)
    formSubmissions = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    
    if len(clientForms) > 0:
        clientForms = ast.literal_eval(clientForms[0].formData)
        existing = True
    else:
        clientForms = 'none'
    print(clientForms)
    finalList = {'Daily':[], 'Weekly':[], 'Monthly':[], 'Quarterly':[], 'Annually':[]}
    
    
    for formInfo in clientForms:
        print("Cross Reference " + str(formInfo[0]) + "...")
        for x in allForms:
            print("With " + str(x.id) + "...")
            for submissions in formSubmissions:
                if formInfo[0] == x.id and submissions.formID.id == x.id:
                        print("Found a MATCH! Adding to finalList.")
                        formTitle = x.header + ' - ' + x.title
                        if x.frequency == 'Daily':
                            finalList['Daily'].append((formInfo[1], formTitle, submissions.submitted))
                        elif x.frequency == 'Weekly':
                            finalList['Weekly'].append((formInfo[1], formTitle, submissions.submitted))
                        elif x.frequency == 'Monthly':
                            finalList['Monthly'].append((formInfo[1], formTitle, submissions.submitted))
                        elif x.frequency == 'Quarterly':
                            finalList['Quarterly'].append((formInfo[1], formTitle, submissions.submitted))
                        elif x.frequency == 'Anually':
                            finalList['Annually'].append((formInfo[1], formTitle, submissions.submitted))
    
    # if existing:
    #     for form in allForms:
    #         formTitle = form.header + ' - ' + form.title
    #         if form.frequency == 'Daily':
    #             finalList['Daily'].append((form.form, formTitle, form.submitted))
    #         elif form.frequency == 'Weekly':
    #             finalList['Weekly'].append((form.form, formTitle, form.submitted))
    #         elif form.frequency == 'Monthly':
    #             finalList['Monthly'].append((form.form, formTitle, form.submitted))
    #         elif form.frequency == 'Quarterly':
    #             finalList['Quarterly'].append((form.form, formTitle, form.submitted))
    #         elif form.frequency == 'Anually':
    #             finalList['Annually'].append((form.form, formTitle, form.submitted))
       
    for each in finalList:
        if len(finalList[each]) == 0:
            finalList[each] = 'No forms added'
        else:
            def myFunc(e):
                return e[0]
            finalList[each].sort(key=myFunc)
                
    print(finalList)
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard', answer['facilitySelect'])
    return render(request, 'supervisor/formsProgress.html', {
        'notifs': notifs, 
        'finalList': finalList, 
        'facility': facility, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'sortedFacilityData': sortedFacilityData
    })