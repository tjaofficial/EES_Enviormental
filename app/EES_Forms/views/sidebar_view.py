from django.shortcuts import render, redirect
from ..models import user_profile_model, issues_model, Forms, Event, daily_battery_profile_model, User, sop_model, formA1_readings_model, formA2_model, formA3_model, formA4_model, formA5_readings_model, bat_info_model, formM_model
from ..forms import issues_form, events_form, sop_form
import datetime
import calendar
from django.core.exceptions import FieldError
from django.db.models import Q
from django.apps import apps
from ..utils import Calendar
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from .print_form_view import date_change
from EES_Forms.views.supervisor_view import getCompanyFacilities
lock = login_required(login_url='Login')


@lock
def corrective_action_view(request, facility):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    
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
    return render(request, "ees_forms/corrective_actions.html", {
        "varPull": varPull, 'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'ca_forms': ca_forms, 'profile': profile, 'client': client, "supervisor": supervisor, "unlock": unlock, 
    })

@lock
def calendar_view(request, facility, year, month):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    options = bat_info_model.objects.all()
    profile = user_profile_model.objects.all()
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
    html_cal = calend.formatmonth(year, month_number, year, withyear=True)
    sortedFacilityData = getCompanyFacilities(request.user.username)
    return render(request, "ees_forms/schedule.html", {
        'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, "supervisor": supervisor, 'year': year, 'month': month, 'prev_month': prev_month, 'next_month': next_month, 'events': events, 'html_cal': html_cal, 'prev_year': prev_year, 'next_year': next_year, 'profile': profile, 'unlock': unlock, 'client': client,
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
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    options = bat_info_model.objects.all()
    profile = user_profile_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if request.method == 'POST':
        answer = request.POST
        print(answer)
        if answer['facilitySelect'] != '':
            return redirect('archive', answer['facilitySelect'])

    return render(request, 'ees_forms/ees_archive.html', {
        'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'profile': profile, 'client': client, "supervisor": supervisor, "unlock": unlock, 
    })

@lock
def search_forms_view(request, facility, access_page):
    readingsData = False
    ModelForms = Forms.objects.all()
    weekend = False
    unlock = False
    client = False
    supervisor = False
    monthList =''
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    options = bat_info_model.objects.all()
    profile = user_profile_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
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
        searched = request.POST['searched']
        database = ''
        database2 = ''
        att_check = ''
        mainList = ''
        weekend = False

        form_list = Forms.objects.filter(Q(form__icontains=searched) | Q(frequency__icontains=searched) | Q(title__icontains=searched))

        forms = form_list.filter(facilityChoice__facility_name=facility).order_by('form')
        letterForms = []
        otherForms = []
        for x in forms:
            if len(x.form) <= 3:
                letterForms.append([x.form.replace('-',''), 'form' + x.form.replace('-','') + '_model', x])
            else:
                otherForms.append([x.form.replace(' ', '_'), x.form.replace(' ', '_').lower() + '_model', x])

        return render(request, 'ees_forms/search_forms.html', {
            'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'unlock': unlock, 'supervisor': supervisor, 'letterForms': letterForms, 'otherForms': otherForms, 'mainList': mainList, 'readingsData': readingsData, 'profile': profile, 'searched': searched, 'forms': forms, 'access_page': access_page, 'database': database, 'database2': database2,  'att_check': att_check, 'weekend': weekend,  'client': client,
        })
    else:
        return render(request, 'ees_forms/search_forms.html', {
            'sortedFacilityData': sortedFacilityData, 'monthList': monthList, 'options': options, 'facility': facility, 'unlock': unlock, 'supervisor': supervisor, 'mainList': mainList, 'readingsData': readingsData, 'profile': profile, 'access_page': access_page, 'database': database, 'database2': database2, 'att_check': att_check, 'weekend': weekend, 'client': client,
        })

@lock
def issues_view(request, facility, form_name, form_date, access_page):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    print(str(form_date))
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]
    options = bat_info_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.username)
    if access_page == 'form':
        data = Forms.objects.all()
        today = datetime.date.today()
        if today.weekday() == 5:
            day = 'saturday'
        elif today.weekday() == 6:
            day = 'sunday'
        for x in data:
            if x.form == form_name:
                if x.form in {'O', 'P'}:
                    link = x.frequency + '/' + x.link + '/' + access_page + '/' + day
                else:
                    link = x.frequency + '/' + x.link + '/' + access_page
                    
                    
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

                done = Forms.objects.filter(form=form_name)[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms', facility)
    elif access_page == 'issue':
        org = issues_model.objects.filter(date__exact=form_date)
        database_form = org[0]
        print('CHECK 1')
        for entry in org:
            if datetime.datetime.strptime(form_date, '%Y-%m-%d').date() == entry.date:
                if form_name == entry.form:
                    print('CHECK 3')
                    picker = entry
                    form = issues_form()
                    link = ''
                    if client:
                        entry.viewed = True
                        entry.save()
    elif access_page == 'edit':
        org = issues_model.objects.all().order_by('-date')
        database_form = org[0]
        for entry in org:
            if datetime.datetime.strptime(form_date, '%Y-%m-%d').date() == entry.date:
                print('check 1')
                if form_name == entry.form:
                    print('check 2')
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
            data = issues_form(request.POST, instance=picker)
            if data.is_valid():
                data.save()

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
            if existing:
                data = issues_form(request.POST, instance=database_form)
            else:
                data = issues_form(request.POST)
            if data.is_valid():
                data.save()

                done = Forms.objects.filter(form=form_name)[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms', facility)
    return render(request, "ees_forms/issues_template.html", {
        'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'form': form, 'access_page': access_page, 'picker': picker, 'form_name': form_name, "form_date": form_date, 'link': link, 'profile': profile, "unlock": unlock, "client": client, "supervisor": supervisor
    })

@lock
def event_add_view(request, facility):
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    options = bat_info_model.objects.all()    
    today = datetime.date.today()
    profile = user_profile_model.objects.all()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    sortedFacilityData = getCompanyFacilities(request.user.username)
    form_var = events_form()

    if request.method == "POST":
        request_form = events_form(request.POST)
        if request_form.is_valid():
            request_form.save()

            cal_link = 'schedule/' + str(today_year) + '/' + today_month

            return redirect(cal_link)

    return render(request, "ees_forms/event_add.html", {
        'sortedFacilityData': sortedFacilityData,'options': options, 'facility': facility, 'today_year': today_year, 'today_month': today_month, 'form': form_var, 'profile': profile, 'supervisor': supervisor, "client": client, 'unlock': unlock, 
    })

@lock
def event_detail_view(request, facility, access_page, event_id):
    today = datetime.date.today()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    supervisor = False
    options = bat_info_model.objects.all()
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
        
    context = {}
    if supervisor:
        context['parent_template'] = 'admin/sup_layout.html'
    else:
        context['parent_template'] = 'ees_forms/layout.html'

    form = events_form()
    if access_page == 'view':
        my_event = Event.objects.get(pk=event_id)
    elif access_page == 'edit':
        data_pull = Event.objects.get(pk=event_id)
        initial_data = {
            'observer': data_pull.observer,
            'title': data_pull.title,
            'date': data_pull.date,
            'start_time': data_pull.start_time,
            'end_time': data_pull.end_time,
            'notes': data_pull.notes,
        }
        my_event = events_form(initial=initial_data)

        if request.method == 'POST':
            data = events_form(request.POST, instance=data_pull)
            print('pork')
            if data.is_valid():
                print('chicken')
                data.save()

                return redirect('../../event_detail/' + str(event_id) + '/view')

    return render(request, "ees_forms/event_detail.html", {
        'options': options, 'facility': facility, 'context': context, "supervisor": supervisor, 'today_year': today_year, 'today_month': today_month, 'form': form, 'my_event': my_event, 'event_id': event_id, 'access_page': access_page
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
    options = bat_info_model.objects.all()
    unlock = False
    client = False
    supervisor = False
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    Users = User.objects.all()
    profile = user_profile_model.objects.order_by('user')
    
    
    sortedFacilityData = getCompanyFacilities(request.user.username)
    form_enteredA1 = False
    form_enteredA2 = False
    form_enteredA3 = False
    form_enteredA4 = False
    form_enteredA5 = False
    formA1 = formA1_readings_model.objects.all().order_by('-form')
    formA2 = formA2_model.objects.all().order_by('-date')
    formA3 = formA3_model.objects.all().order_by('-date')
    formA4 = formA4_model.objects.all().order_by('-date')
    formA5 = formA5_readings_model.objects.all().order_by('-form')
    now = datetime.datetime.now()
    year = str(now.year)
    if len(str(now.month)) == 1:
        month = "0" + str(now.month)
    else:
        month = str(now.month)
    if len(str(now.day)) == 1:
        day = '0' + str(now.day)
    else:
        day = str(now.day)
    date = year + '-' + month + '-' + day
    today = datetime.date.today()
    if len(formA1) > 0:
        most_recent_A1 = formA1[0].form.date
        if most_recent_A1 == today:
            form_enteredA1 = True
    if len(formA2) > 0:
        most_recent_A2 = formA2[0].date
        if most_recent_A2 == today:
            form_enteredA2 = True
    if len(formA3) > 0:
        most_recent_A3 = formA3[0].date
        if most_recent_A3 == today:
            form_enteredA3 = True
    if len(formA4) > 0:
        most_recent_A4 = formA4[0].date
        if most_recent_A4 == today:
            form_enteredA4 = True
    if len(formA5) > 0:
        most_recent_A5 = formA5[0].form.date
        if most_recent_A5 == today:
            form_enteredA5 = True
    
    
    
    organized_list = []
    for index, user in enumerate(profile):
        if user.certs:
            certList = user.certs.split(',')
            i = 0
            for item in certList:
                certList[i] = certList[i].strip()
                i += 1
            organized_list.append((user.id, user, certList, handlePhone(user.phone)))
        else:
            organized_list.append((user.id, user, 'N/A' , handlePhone(user.phone)))
    
    print(organized_list)
    
    return render(request, "shared/contacts.html", {
        'sortedFacilityData': sortedFacilityData, 'options': options, 'facility': facility, 'profile': profile, 'organized_list': organized_list, 'supervisor': supervisor, "client": client, 'unlock': unlock, 'form_enteredA5': form_enteredA5, 'form_enteredA4': form_enteredA4, 'form_enteredA3': form_enteredA3, 'form_enteredA2': form_enteredA2,'form_enteredA1': form_enteredA1, 'date': date
    })
    
@lock
def sop_view(request, facility):
    unlock = False
    client = False
    supervisor = False
    options = bat_info_model.objects.all()
    if request.user.groups.filter(name=OBSER_VAR):
        unlock = True
    if request.user.groups.filter(name=CLIENT_VAR):
        client = True
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    sops = sop_model.objects.all().order_by('name')
    sopForm = sop_form()
    
    if request.method == 'POST':
        form = sop_form(request.POST, request.FILES)
        if os.path.exists("./media/SOPs/" + request.POST['pdf_link']):
            ('EXISTS')
        else:
            if form.is_valid():
                form.save()
                print('SAVED')
            else:
                print('NOT SAVED')
            
    return render(request, 'shared/sops.html', {
        'options': options, 'facility': facility, 'sops': sops, 'sopForm': sopForm, 'supervisor': supervisor, "client": client, 'unlock': unlock
    })