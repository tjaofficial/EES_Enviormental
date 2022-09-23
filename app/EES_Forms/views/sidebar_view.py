from django.shortcuts import render, redirect
from ..models import user_profile_model, issues_model, Forms, Event, daily_battery_profile_model, User, sop_model, formA1_readings_model, formA2_model, formA3_model, formA4_model, formA5_readings_model
from ..forms import issues_form, events_form, sop_form
import datetime
import calendar
from django.core.exceptions import FieldError
from django.db.models import Q
from django.apps import apps
from ..utils import Calendar
from django.contrib.auth.decorators import login_required
import os

lock = login_required(login_url='Login')


@lock
def corrective_action_view(request):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True

    profile = user_profile_model.objects.all()

    ca_forms = issues_model.objects.all().order_by('-id')

    return render(request, "ees_forms/corrective_actions.html", {
        'ca_forms': ca_forms, 'profile': profile, 'client': client, "admin": admin, "unlock": unlock, 
    })

@lock
def calendar_view(request, year, month):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    
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

    return render(request, "ees_forms/schedule.html", {
        "admin": admin, 'year': year, 'month': month, 'prev_month': prev_month, 'next_month': next_month, 'events': events, 'html_cal': html_cal, 'prev_year': prev_year, 'next_year': next_year, 'profile': profile, 'unlock': unlock, 'client': client,
    })

@lock
def schedule_view(request):
    admin = False
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    today_year = int(datetime.date.today().year)
    today_month = str(calendar.month_name[datetime.date.today().month])

    return redirect('schedule/' + str(today_year) + '/' + str(today_month))

    return render(request, "ees_forms/scheduling.html", {
        'today_year': today_year, 'today_month': today_month, 'admin': admin,
    })

@lock
def archive_view(request):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True

    profile = user_profile_model.objects.all()

    return render(request, 'ees_forms/ees_archive.html', {
        'profile': profile, 'client': client, "admin": admin, "unlock": unlock, 
    })

@lock
def search_forms_view(request, access_page):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    profile = user_profile_model.objects.all()
    if access_page != 'search':
        Model = apps.get_model('EES_Forms', access_page)
        ModelForms = Forms.objects.all()
        chk_database = Model.objects.count()
        weekend = False

        if chk_database == 0:
            att_check = 5
        else:
            try:
                database = Model.objects.all().order_by('-date')
                for x in ModelForms:
                    if x.form == access_page[4]:
                        if x.frequency[0] == 'W':
                            att_check = 4
                            if x.weekend_only:
                                weekend = True
                            else:
                                weekend = False
                        else:
                            att_check = 1
                            print('no')
                    elif x.form == access_page[4] + '-' + access_page[5]:
                        if x.frequency[0] == 'W':
                            att_check = 4
                        else:
                            att_check = 1
                    else:
                        print('Error - EES_00005')
            except FieldError as e:
                database = Model.objects.all().order_by('-week_start')
                for x in ModelForms:
                    if x.form == access_page[4]:
                        if x.frequency[0] == 'D':
                            att_check = 3
                        else:
                            att_check = 2
                    elif x.form == access_page[4] + '-' + access_page[5]:
                        if x.frequency[0] == 'D':
                            att_check = 3
                        else:
                            att_check = 2
                    print('Error - EES_00006')

    if request.method == "POST":
        searched = request.POST['searched']
        database = ''
        att_check = ''
        weekend = False

        form_list = Forms.objects.filter(Q(form__icontains=searched) | Q(frequency__icontains=searched) | Q(title__icontains=searched))

        forms = form_list.order_by('form')

        return render(request, 'ees_forms/search_forms.html', {
            'profile': profile, 'searched': searched, 'forms': forms, 'access_page': access_page, 'database': database, 'att_check': att_check, 'weekend': weekend,  'client': client,
        })
    else:
        return render(request, 'ees_forms/search_forms.html', {
            'profile': profile, 'access_page': access_page, 'database': database, 'att_check': att_check, 'weekend': weekend, 'client': client,
        })

@lock
def issues_view(request, form_name, form_date, access_page):
    unlock = False
    if request.user.groups.filter(name='SGI Technician') or request.user.is_superuser:
        unlock = True
    print(str(form_date))
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    todays_log = daily_prof[0]

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
        initial_data = {
                'date': todays_log.date_save,
                'form': form_name
            }
        picker = ''
        form = issues_form(initial=initial_data)
        if request.method == "POST":
            data = issues_form(request.POST)
            if data.is_valid():
                data.save()

                done = Forms.objects.filter(form=form_name)[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
    elif access_page == 'issue':
        org = issues_model.objects.filter(date__exact=form_date)
        database_form = org[0]
        print(org[0].form)
        print('CHECK 1')
        for entry in org:
            if str(form_date) == str(entry.date):
                print('CHECK 2')
                print(form_name)
                print(entry.form)
                if form_name == entry.form:
                    print('CHECK 3')
                    picker = entry
                    form = issues_form()
                    link = ''
    elif access_page == 'edit':
        org = issues_model.objects.all().order_by('-date')
        database_form = org[0]
        for entry in org:
            if str(form_date) == str(entry.date):
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

                return redirect('IncompleteForms')
    return render(request, "ees_forms/issues_template.html", {
        'form': form, 'access_page': access_page, 'picker': picker, 'form_name': form_name, "form_date": form_date, 'link': link, 'profile': profile, "unlock": unlock
    })

@lock
def event_add_view(request):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
        
    today = datetime.date.today()
    profile = user_profile_model.objects.all()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])

    form_var = events_form()

    if request.method == "POST":
        request_form = events_form(request.POST)
        if request_form.is_valid():
            request_form.save()

            cal_link = 'schedule/' + str(today_year) + '/' + today_month

            return redirect(cal_link)

    return render(request, "ees_forms/event_add.html", {
        'today_year': today_year, 'today_month': today_month, 'form': form_var, 'profile': profile, 'admin': admin, "client": client, 'unlock': unlock, 
    })

@lock
def event_detail_view(request, access_page, event_id):
    today = datetime.date.today()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    admin = False
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
        
    context = {}
    if admin:
        context['parent_template'] = 'admin/admin_layout.html'
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
        'context': context, "admin": admin, 'today_year': today_year, 'today_month': today_month, 'form': form, 'my_event': my_event, 'event_id': event_id, 'access_page': access_page
    })

@lock
def shared_contacts_view(request):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
    Users = User.objects.all()
    profile = user_profile_model.objects.order_by('user')
    
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
        organized_list.append((index, user))
    
    
    
    return render(request, "shared/contacts.html", {
        'profile': profile, 'organized_list': organized_list, 'admin': admin, "client": client, 'unlock': unlock, 'form_enteredA5': form_enteredA5, 'form_enteredA4': form_enteredA4, 'form_enteredA3': form_enteredA3, 'form_enteredA2': form_enteredA2,'form_enteredA1': form_enteredA1, 'date': date
    })
    
def sop_view(request):
    unlock = False
    client = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
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
        'sops': sops, 'sopForm': sopForm, 'admin': admin, "client": client, 'unlock': unlock
    })