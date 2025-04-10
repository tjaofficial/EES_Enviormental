from django.shortcuts import render, redirect # type: ignore
from ..models import user_profile_model, issues_model, Forms, Event, daily_battery_profile_model, User, sop_model, facility_model, form22_model, formSubmissionRecords_model, form_settings_model
from ..forms import issues_form, events_form, sop_form, user_profile_form, UserChangeForm
import datetime
import calendar
from django.core.exceptions import FieldError # type: ignore
from django.db.models import Q # type: ignore
from django.apps import apps # type: ignore
from ..utils import Calendar, updateSubmissionForm, setUnlockClientSupervisor, colorModeSwitch, checkIfFacilitySelected, getCompanyFacilities,get_facility_forms, createNotification, setUnlockClientSupervisor
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR, USE_S3
import os
from django.utils.text import slugify # type: ignore
from django.http import JsonResponse # type: ignore
import json
from django.views.decorators.csrf import csrf_exempt # type: ignore

lock = login_required(login_url='Login')


@lock
def corrective_action_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
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
            ca_forms = ca_forms.filter(formChoice__formChoice__form__icontains=issueForm_query)
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
    options = facility_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if answer['facilitySelect'] != '':
            return redirect('Corrective-Action', answer['facilitySelect'])
    return render(request, "shared/corrective_actions.html", {
        'notifs': notifs, 
        "varPull": varPull, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        'facility': facility, 
        'ca_forms': ca_forms, 
        'profile': profile, 
        'client': client, 
        "supervisor": supervisor, 
        "unlock": unlock, 
    })

@lock
def calendar_view(request, facility, year, month):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    options = facility_model.objects.all()
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
    options = facility_model.objects.all()
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
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    options = facility_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    archiveForm_query = request.GET.get('archiveFormID')
    archiveFormLabel_query = request.GET.get('archiveFormLabel')
    archiveMonth_query = request.GET.get('archiveMonth')
    archiveDate_query = request.GET.get('archiveDate')
    formSettingsModel = form_settings_model.objects.filter(facilityChoice__facility_name=facility, settings__active='true')
    varPull = [
        archiveForm_query,
        archiveMonth_query,
        archiveDate_query,
    ]
    
    def getFsSearchID(itemSearched, fsModel):
        if itemSearched != '' and itemSearched is not None and fsModel.exists():
            fsList = []
            idSearchData = False
            itemSearched = int(itemSearched)
            print('check 1')
            print(fsModel)
            for fs in fsModel:
                print(int(fs.formChoice.form))
                print(itemSearched)
                if int(fs.formChoice.form) == itemSearched:
                    idSearchData = fs
                    break
            if idSearchData:
                link = str(idSearchData.formChoice.link) + '_model'
                chk_database = apps.get_model('EES_Forms', link).objects.filter(formSettings__facilityChoice__facility_name=facility)
                for item in chk_database:
                    fsList.append(item)
            return fsList
        else:
            return "none"
    
    def getFsSearchLabel(itemSearched, fsModel):
        if itemSearched != '' and itemSearched is not None and fsModel.exists():
            fsList1 = []
            print('Starting to search labels...')
            for fs in fsModel:
                fsPackets = fs.settings['packets']
                for packetLabel in fsPackets:
                    if fsPackets[packetLabel].lower() == itemSearched.lower():
                        if fs not in fsList1:
                            fsList1.append(fs)
            print(fsList1)
            modelsList = []
            for fsSort in fsList1:
                for model in apps.get_models():
                    if model.__name__[:4] == "form" and model.__name__[-6:] == '_model':
                        modelName = model.__name__[4:-6]
                        if str(modelName) == str(fsSort.formChoice.form):
                            modelsList.append((model, fsSort))
            fsList = []
            for item in modelsList:
                chk_database = item[0].objects.filter(formSettings=item[1])
                for iForm in chk_database:
                    if iForm not in fsList:
                        fsList.append(iForm)
            return fsList  
        else:
            return "none"
                            
    def getFsSearchMonthYear(itemSearched, fsModel):
        if itemSearched != "" and itemSearched is not None and fsModel.exists():
            itemSearched = datetime.datetime.strptime(itemSearched, "%Y-%m").date()
            # formIDList = []
            # for fs in fsModel:
            #     formIDList.append((fs.formChoice.id, fs))
            # print(formIDList)
            modelsList = []
            for model in apps.get_models():
                for fs in fsModel:
                    if model.__name__[:4] == "form" and model.__name__[-6:] == '_model':
                        modelName = model.__name__[4:-6]
                        if str(modelName) == str(fs.formChoice.form):
                            modelsList.append((model, fs))
            fsList = []
            for item in modelsList:
                try:
                    chk_database = item[0].objects.filter(Q(date__month=itemSearched.month) & Q(date__year=itemSearched.year))
                except:
                    chk_database = item[0].objects.filter(Q(week_start__month=itemSearched.month) & Q(week_start__year=itemSearched.year))
                for iForm in chk_database:
                    if iForm not in fsList:
                        fsList.append(iForm)
            return fsList  
        else:
            return "none"
 
    def getFsSearchDate(itemSearched, fsModel):
        if itemSearched != "" and itemSearched is not None and fsModel.exists():
            itemSearched = datetime.datetime.strptime(itemSearched, "%Y-%m-%d").date()
            modelsList = []
            for model in apps.get_models():
                for fs in fsModel:
                    if model.__name__[:4] == "form" and model.__name__[-6:] == '_model':
                        modelName = model.__name__[4:-6]
                        if str(modelName) == str(fs.formChoice.form):
                            modelsList.append((model, fs))
            fsList = []
            for item in modelsList:
                try:
                    chk_database = item[0].objects.filter(date=itemSearched)
                except:
                    chk_database = item[0].objects.filter(week_start=itemSearched)
                for iForm in chk_database:
                    if iForm not in fsList:
                        fsList.append(iForm)
            return fsList  
        else:
            return "none"
      
    IDQueryList = getFsSearchID(archiveForm_query, formSettingsModel)
    labelQueryList = getFsSearchLabel(archiveFormLabel_query, formSettingsModel)
    monthYearQueryList = getFsSearchMonthYear(archiveMonth_query, formSettingsModel)
    dateQueryList = getFsSearchDate(archiveDate_query, formSettingsModel)
    
    sortList = []
    finalList = []
    if monthYearQueryList != 'none':
        finalList = monthYearQueryList
    if IDQueryList != 'none':
        if len(finalList) == 0:
            finalList = IDQueryList
        else:
            for sort2 in IDQueryList:
                if sort2 in finalList:
                    sortList.append(sort2)
            finalList = sortList
            sortList = []
    if labelQueryList != 'none':
        if len(finalList) == 0:
            finalList = labelQueryList
        else:
            for sort3 in labelQueryList:
                if sort3 in finalList:
                    sortList.append(sort3)
            finalList = sortList
            sortList = []
    if dateQueryList != 'none':
        if len(finalList) == 0:
            finalList = dateQueryList
        else:
            for sort4 in dateQueryList:
                if sort4 in finalList:
                    sortList.append(sort4)
            finalList = sortList
    if request.method == 'POST':
        answer = request.POST
        if supervisor:
            if answer['facilitySelect'] != '':
                return redirect('archive', answer['facilitySelect'])
        else:
            if 'colorMode' in answer.keys():
                colorModeSwitch(request)

    return render(request, 'shared/archive.html', {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        'facility': facility,
        'client': client, 
        "supervisor": supervisor, 
        "unlock": unlock, 
        'finalList': finalList,
    })

@lock
def search_forms_view(request, facility, access_page):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    readingsData = False
    ModelForms = Forms.objects.all()
    weekend = False
    monthList =''
    options = facility_model.objects.all()
    profile = user_profile_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    facilityForms = get_facility_forms('facilityName', facility)
    formSettingsModel = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    formSubs = formSubmissionRecords_model.objects.filter(facilityChoice__facility_name=facility)
    if access_page != 'search':
        fsID = int(access_page.split("-")[1])
        access_page = access_page[:-4]
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
                            if x.form == access_page[4] or x.form == access_page[4] + '-' + access_page[5] or x.form == access_page[0:-6].replace('_', ' ').title() or x.link == access_page[:6]:
                                print("The follow model can be used to find forms:")
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
                                print('-')
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
                            if x.form == access_page[4] or x.form == access_page[4] + '-' + access_page[5] or x.link == access_page[:6]:
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
                        print(mainList)
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
            queryN = form22_model.objects.all().filter(facilityChoice__facility_name=facility)
            monthList = []
            eliminator =[]
            for month in queryN:
                if month.date.month not in eliminator:
                    monthList.append((month.date.month, month.date.year, calendar.month_name[month.date.month],))
                    eliminator.append(month.date.month)
            print(monthList)
    else:
        mainList = ''
        fsID = ''
    if request.method == "POST":
        print('found it----------------')
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
            form_list = formSettingsModel.filter(Q(formChoice__form__icontains=searchedText) | Q(formChoice__frequency__icontains=searchedText) | Q(formChoice__title__icontains=searchedText)).order_by('id')
            #form_list = formSubs.filter(Q(formID__form__icontains=searchedText) | Q(formID__frequency__icontains=searchedText) | Q(formID__title__icontains=searchedText)).order_by('formID')
            print(form_list)
            forms = []
            for settignsEntry in form_list:
                for facilityForm in facilityForms:
                    if settignsEntry.id == facilityForm:
                        forms.append(settignsEntry)
                        #forms.append((facilityForm, settignsEntry))
            # forms = form_list
            print(forms)
            letterForms = []
            for x in forms:
                if x.formChoice.id not in {26,27}:
                    modelTry1 = 'form' + x.formChoice.form.replace('-','') + '_model'
                    modelTry2 = x.formChoice.link + '_model'
                else:
                    modelTry1 = x.formChoice.form.replace(' ', '_').lower() + '_model'
                    modelTry2 = x.formChoice.link + '_model'
                try:
                    chk_database = apps.get_model('EES_Forms', modelTry1).objects.count()
                    newModelName = True
                except:
                    chk_database = apps.get_model('EES_Forms', modelTry2).objects.count()
                    newModelName = False
                if newModelName:
                    if x.formChoice.id not in {26,27}:
                        letterForms.append([x, 'form' + x.formChoice.form.replace('-','') + '_model', x.formChoice])
                    else:
                        letterForms.append([x, x.formChoice.form.replace(' ', '_').lower() + '_model', x.formChoice])
                else:
                    if x.formChoice.id not in {26,27}:
                        letterForms.append([x, x.formChoice.link + '_model', x.formChoice])
                    else:
                        letterForms.append([x, x.formChoice.link + '_model', x.formChoice])
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
            'fsID': fsID,
            #'database': database, 
            #'database2': database2, 
            #'att_check': att_check, 
            'weekend': weekend, 
            'client': client,
        })

@lock
def issues_view(request, facility, fsID, form_date, access_page):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    profile = user_profile_model.objects.get(user=request.user)
    now = datetime.datetime.now().date()
    todays_log = daily_battery_profile_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date_save')
    options = facility_model.objects.all()
    issueModel = issues_model.objects.filter(facilityChoice__facility_name=facility).order_by('-date')
    sortedFacilityData = getCompanyFacilities(request.user.username)
    facilityForms = get_facility_forms('facilityName', facility)
    existing = False
    complince = False
    notifSelector = ['corrective', 'submitted']
    if access_page[-1] == 'c':
        compliance = True
        notifSelector.append('compliance')
        access_page = access_page[:-2]
    else:
        compliance = False
    if todays_log.exists():
        todays_log = todays_log[0]
    formSetting= form_settings_model.objects.get(id=fsID)

    def create_link_elements():
        for facForms in facilityForms:
            settingsID = int(facForms)
            if settingsID == formSetting.id:
                formID = int(formSetting.formChoice.id)
                main_url = formSetting.formChoice.frequency + '/' + str(formID) + '/' + str(fsID) + '/'
                if formSetting.formChoice.id in {24,25}:
                    weekendNameDict = {5:'saturday', 6: 'sunday'}
                    today = datetime.date.today().weekday()
                    for dayNumber in weekendNameDict:
                        if today == dayNumber:
                            day = weekendNameDict[dayNumber]
                else:
                    day = False
            else:
                continue
            return main_url, day, formID, settingsID
    if access_page == 'form':
        main_url, day, formID, settingsID = create_link_elements()
        if day:
            link = main_url + access_page + '/' + day
        else:
            link = main_url + access_page
        existing = False
        picker = 'n/a'
        
        if issueModel.exists():
            database_form = issueModel[0]
            if todays_log.date_save == database_form.date:
                if database_form.formChoice.id == settingsID:
                    existing = True
        if existing:
            initial_data = {
                'formChoice': database_form.formChoice,
                'issues': database_form.issues,
                'notified': database_form.notified,
                'time': database_form.time,
                'date': database_form.date,
                'cor_action': database_form.cor_action
            }
        else:
            print("check 1")
            initial_data = {
                'date': todays_log.date_save,
                'formChoice': form_settings_model.objects.get(id=settingsID)
            }
            print(initial_data)
            picker = ''
        form = issues_form(initial=initial_data)
        if request.method == "POST":
            dataCopy = request.POST.copy()
            dataCopy["facilityChoice"] = options.filter(facility_name=facility)[0]
            dataCopy["out_of_compliance"] = compliance
            dataCopy["userChoice"] = profile
            if existing:
                data = issues_form(dataCopy, instance=database_form)
            else:
                dataCopy['formChoice'] = formSetting
                data = issues_form(dataCopy)
            if data.is_valid():
                data.save()
                for notifSel in notifSelector:
                    createNotification(facility, request, fsID, now, notifSel, data.save())
                updateSubmissionForm(fsID, True, todays_log.date_save)
                return redirect('IncompleteForms', facility)
    elif access_page == 'issue':
        main_url, day, formID, settingsID = create_link_elements()
        if day:
            link = main_url + form_date + '/' + day
        else:
            link = main_url + form_date
        org = issues_model.objects.filter(date__exact=form_date)
        database_form = org[0]
        for entry in org:
            if datetime.datetime.strptime(form_date, '%Y-%m-%d').date() == entry.date:
                if int(fsID) == int(entry.formChoice.id):
                    existing = True
                    picker = entry
                    form = issues_form()
                    if client:
                        entry.viewed = True
                        entry.save()
    elif access_page == 'edit' or access_page == 'resubmit':
        org = issues_model.objects.filter(formChoice=formSetting).order_by('-date')
        database_form = org[0]
        for entry in org:
            if datetime.datetime.strptime(form_date, '%Y-%m-%d').date() == entry.date:
                picker = entry
                link = ''
                existing=True
        initial_data = {
            'form': picker.formChoice.formChoice.id,
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
            dataCopy["out_of_compliance"] = compliance
            data = issues_form(dataCopy, instance=picker)
            if data.is_valid():
                data.save()
                print(data.save().id)
                if access_page == 'resubmit':
                    for notifSel in notifSelector:
                        createNotification(facility, request, fsID, now, notifSel, data.save())
                    updateSubmissionForm(fsID, True, picker.date)
                    return redirect('IncompleteForms', facility)
                else:
                    return redirect('issues_view', facility, fsID, form_date, 'issue')
    else:
        existing = False
        picker = 'n/a'
        if issues_model.objects.count() != 0:
            org = issues_model.objects.all().order_by('-date')
            database_form = org[0]
            if todays_log.date_save == database_form.date:
                if database_form.formChoice.formChoice.id == fsID:
                    existing = True

    if existing:
        initial_data = {
            'form': database_form.formChoice.formChoice.id,
            'issues': database_form.issues,
            'notified': database_form.notified,
            'time': database_form.time,
            'date': database_form.date,
            'cor_action': database_form.cor_action
        }
    else:
        initial_data = {
            'date': todays_log.date_save,
            'formChoice': form_settings_model.objects.get(id=settingsID)
        }

    form = issues_form(initial=initial_data)

    # if request.method == "POST":
    #     dataCopy = request.POST.copy()
    #     dataCopy["facilityChoice"] = options.filter(facility_name=facility)[0]
    #     if existing:
    #         data = issues_form(dataCopy, instance=database_form)
    #     else:
    #         data = issues_form(dataCopy)
    #     if data.is_valid():
    #         print('check #1')
    #         data.save()
    #         createNotification(facility, request, fsID, now, 'submitted')
    #         createNotification(facility, request, fsID, now, 'corrective')
    #         updateSubmissionForm(fsID, True, todays_log.date_save)
    #         return redirect('IncompleteForms', facility)

    return render(request, "shared/issues_template.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        'facility': facility, 
        'form': form, 
        'access_page': access_page, 
        'picker': picker, 
        "form_date": form_date, 
        'link': link, 
        'profile': profile, 
        "unlock": unlock, 
        "client": client, 
        "supervisor": supervisor,
        "initial_data": initial_data
    })

@lock
def event_add_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    options = facility_model.objects.all()
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
def profile_edit_view(request, facility, userID):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if client:
        return redirect('c_dashboard')
    elif unlock:
        return redirect('IncompleteForms', facility)
    
    user_profiles = user_profile_model.objects.all()
    pic = ''
    
    if user_profiles.filter(user__id__exact=userID).exists():
        userProfileInfo = user_profiles.get(user__id__exact=userID)
        userInfo = User.objects.all().get(id__exact=userID)
        pic = userProfileInfo.profile_picture
        if userProfileInfo.phone:
            number = userProfileInfo.phone[2:]
            first = number[:3]
            middle = number[3:6]
            end = number[6:]
            parseNumber = '(' + first + ')' + middle + '-'+ end
        else:
            parseNumber = ''
        
    if request.method == 'POST':
        answer = request.POST
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard', answer['facilitySelect'])
        if request.POST.get('edit_user', False):
            print('CHECK 3')
            finalPhone = '+1' + ''.join(filter(str.isdigit, request.POST['phone']))
            new_data = request.POST.copy()
            new_data['phone'] = finalPhone
            new_data['company'] = userProfileInfo.company
            new_data['date_joined'] = userInfo.date_joined
            new_data['is_active'] = userInfo.is_active
            new_data['groups'] = userInfo.groups.all()[0]
            B = UserChangeForm(
                new_data,
                instance=userInfo
            )
            A = user_profile_form(
                new_data, 
                request.FILES, 
                instance=userProfileInfo
            )
            print(A.errors)
            print(B.errors)
            if A.is_valid() and B.is_valid():
                A.save()
                B.save()
                return redirect('Contacts', facility)
    return render(request, "supervisor/profile_edits.html", {
        'facility': facility,
        'notifs': notifs, 
        "unlock": unlock, 
        "client": client, 
        "supervisor": supervisor,
        'pic': pic, 
        'userInfo': userInfo,
        'userProfileInfo': userProfileInfo,
        'parseNumber': parseNumber
    })

@lock
def event_detail_view(request, facility, access_page, event_id):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    today = datetime.date.today()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    options = facility_model.objects.all()
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
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    options = facility_model.objects.all()
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
        if 'facilitySelect' in request.POST.keys():
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
    
def format_sop_file_path(filename):
    # Replace spaces with underscores and fix the filename format
    base, ext = os.path.splitext(filename)
    formatted_filename = slugify(base).replace('-', '_') + ext
    return f'SOPs/{formatted_filename}'  # Set folder to "SOPs/"

@csrf_exempt
def delete_selected_sops(request, facility):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sop_ids = data.get('selected_sops', [])
            
            if sop_ids:
                sop_model.objects.filter(id__in=sop_ids).delete()
                return JsonResponse({'success': True, 'message': 'Selected SOPs deleted successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'No SOPs selected.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@lock
def sop_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    options = facility_model.objects.filter(facility_name=facility)[0]
    sops = sop_model.objects.filter(facilityChoice__facility_name=facility).order_by('name')
    sopForm = sop_form()
    
    if request.method == 'POST':
        if 'facilitySelect' in request.POST.keys():
            if request.POST['facilitySelect'] != '':
                return redirect('sup_dashboard', request.POST['facilitySelect'])
        # copyPost = request.POST.copy()
        # copyPost['facilityChoice'] = options
        # # print(request.FILES.url)
        # form = sop_form(copyPost, request.FILES)
        # print(form.errors)
        # if form.is_valid():
        #     A = form.save(commit=False)

        #     uploaded_file = request.FILES.get('pdf_file')
        #     if uploaded_file:
        #         formatted_path = format_sop_file_path(uploaded_file.name)
        #         A.pdf_file.name = f'{formatted_path}'  # Full S3 path under "media/SOPs/"

        #     A.pdf_url = A.pdf_file.url
        #     A.save()

        #     print("File Name:", A.pdf_file.name)  # Prints the file name
        #     print("File URL:", A.pdf_file.url)
        sop_id = request.POST.get('sop_id')
        name = request.POST.get('name')
        revision_date = request.POST.get('revision_date')
        pdf_file = request.FILES.get('pdf_file')

        if sop_id:  # Update existing SOP
            sop_instance = sop_model.objects.get(id=sop_id)
            sop_instance.name = name
            sop_instance.revision_date = revision_date
            if pdf_file:
                sop_instance.pdf_file = pdf_file  # Save the uploaded file
                sop_instance.save()
                sop_instance.pdf_url = sop_instance.pdf_file.url  # Now get the URL after saving
            sop_instance.save()
        else:  # Add new SOP
            new_sop = sop_model(
                name=name,
                revision_date=revision_date,
                pdf_file=pdf_file,
            )
            new_sop.facilityChoice = options
            new_sop.save()
            new_sop.pdf_url = new_sop.pdf_file.url  # Access URL after saving
            new_sop.save()

        return redirect('Sop', facility=facility)

    return render(request, 'shared/sops.html', {
        'sortedFacilityData':sortedFacilityData, 
        'notifs': notifs, 
        'options': options, 
        'facility': facility, 
        'sops': sops, 
        'sopForm': sopForm, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'AWS': USE_S3
    })
   
@lock 
def formsProgress(request, facility, section):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if unlock:
        return redirect('IncompleteForms', facility)
    formSettingsModel = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    clientForms = get_facility_forms('facilityName', facility)
    finalList = {'Daily':[], 'Weekly':[], 'Monthly':[], 'Quarterly':[], 'Annually':[]}
    freqList = ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Annually']
    for formInfo in clientForms:
        print("Cross Reference " + str(formInfo) + "...")
        for x in formSettingsModel:
            print("With " + str(x.id) + "...")
            if formInfo == x.id:
                print("Found a MATCH! Adding to finalList.")
                formTitle = x.formChoice.header + ' - ' + x.formChoice.title
                if x.formChoice.frequency == 'Daily':
                    finalList['Daily'].append((formInfo, formTitle, x.subChoice.submitted))
                elif x.formChoice.frequency == 'Weekly':
                    finalList['Weekly'].append((formInfo, formTitle, x.subChoice.submitted))
                elif x.formChoice.frequency == 'Monthly':
                    finalList['Monthly'].append((formInfo, formTitle, x.subChoice.submitted))
                elif x.formChoice.frequency == 'Quarterly':
                    finalList['Quarterly'].append((formInfo, formTitle, x.subChoice.submitted))
                elif x.formChoice.frequency == 'Anually':
                    finalList['Annually'].append((formInfo, formTitle, x.subChoice.submitted))
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
        'sortedFacilityData': sortedFacilityData,
        'freqList': freqList
    })