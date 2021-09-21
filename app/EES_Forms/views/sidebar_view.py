from django.shortcuts import render, redirect
from ..models import user_profile_model, issues_model, Forms, Event
import datetime
import calendar
from django.core.exceptions import FieldError
from django.db.models import Q
from django.apps import apps
from ..utils import Calendar


def corrective_action_view(request):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    profile = user_profile_model.objects.all()

    ca_forms = issues_model.objects.all().order_by('-id')

    return render(request, "ees_forms/corrective_actions.html", {
        'ca_forms': ca_forms, 'profile': profile, 'client': client
    })


def calendar_view(request, year, month):
    unlock = False
    client = False
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

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
        'year': year, 'month': month, 'prev_month': prev_month, 'next_month': next_month, 'events': events, 'html_cal': html_cal, 'prev_year': prev_year, 'next_year': next_year, 'profile': profile, 'unlock': unlock, 'client': client,
    })


def schedule_view(request):
    today_year = int(datetime.date.today().year)
    today_month = str(calendar.month_name[datetime.date.today().month])

    return redirect('schedule/' + str(today_year) + '/' + str(today_month))

    return render(request, "ees_forms/scheduling.html", {
        'today_year': today_year, 'today_month': today_month
    })


def archive_view(request):
    client = False
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True

    profile = user_profile_model.objects.all()

    return render(request, 'ees_forms/ees_archive.html', {
        'profile': profile, 'client': client
    })


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
