from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.utils.dateparse import parse_date # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR, USE_S3
from ..utils.main_utils import Calendar, updateSubmissionForm, setUnlockClientSupervisor, colorModeSwitch, checkIfFacilitySelected, getCompanyFacilities, createNotification, setUnlockClientSupervisor
from ..models import facility_model, Event, user_profile_model
from ..forms import events_form
from datetime import datetime
import calendar
import json

lock = login_required(login_url='Login')

@lock
def calendar_view(request, year, month):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    options = facility_model.objects.all()
    profile = request.user.user_profile
    try:
        month_number = int(month)
        month = calendar.month_name[month_number]
    except:
        month = month.title()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)

    prev_month = str(calendar.month_name[12]) if month_number == 1 else str(calendar.month_name[month_number - 1])
    prev_year = str(year - 1) if month_number == 1 else year
    next_month = str(calendar.month_name[1]) if month_number == 12 else str(calendar.month_name[month_number + 1])
    next_year = str(year + 1) if month_number == 12 else year

    events = Event.objects.all()

    calend = Calendar()
    calend.setfirstweekday(6)
    html_cal = calend.formatmonth(year, month_number, year, request.user.user_profile, withyear=True)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard')
    return render(request, "ees_forms/schedule.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        "supervisor": supervisor, 
        'year': year, 
        'month': month, 
        'prev_month': prev_month, 
        'next_month': next_month, 
        'events': events, 
        'html_cal': html_cal, 
        'prev_year': prev_year, 
        'next_year': next_year, 
        'calendars': profile.settings['calendar']['calendars'], 
        'unlock': unlock, 
        'client': client,
        'facility': facility
    })

@lock
def ajax_calendar(request):
    facility = getattr(request, 'facility', None)
    data = json.loads(request.body)
    groups = data.get("groups", [])
    events = Event.objects.filter(facilityChoice=facility, calendarChoice__in=groups) if groups else Event.objects.filter(facilityChoice=facility)
    print(f"These are the event in the filter: {events}")
    data = [
        {
            'id': e.id,
            'title': e.title,
            'start': datetime.combine(e.date, e.start_time).isoformat() if e.start_time else e.date.isoformat(),
            'end':  datetime.combine(e.date, e.end_time).isoformat() if e.end_time else None,
            'allDay': e.allDay,
            'extendedProps': {
                'group': e.calendarChoice,
                'observer': e.observer,
                'repeat': e.repeat,
                'alerts': e.alerts,
                'location': e.facilityChoice.facility_name
            }
        }
        for e in events
    ]
    return JsonResponse(data, safe=False)

@lock
def events_for_day(request):
    facility = getattr(request, 'facility', None)
    date_str = request.GET.get('date')
    date = parse_date(date_str)
    events = Event.objects.filter(facilityChoice=facility, date=date)
    data = [
        {
            'id': e.id,
            'title': e.title,
            'start': datetime.combine(e.date, e.start_time).isoformat() if e.start_time else e.date.isoformat(),
            'end':  datetime.combine(e.date, e.end_time).isoformat() if e.end_time else None,
            'group': e.calendarChoice,
            'allDay': e.allDay,
            'observer': e.observer,
            'repeat': e.repeat,
            'alerts': e.alerts,
            'location': e.facilityChoice.facility_name
        }
        for e in events
    ]
    return JsonResponse(data, safe=False)

@lock
def schedule_view(request):
    supervisor = False
    options = facility_model.objects.all()
    if request.user.groups.filter(name=SUPER_VAR) or request.user.is_superuser:
        supervisor = True
    today_year = int(datetime.now().date().year)
    today_month = str(calendar.month_name[datetime.now().date().month])

    return redirect('Calendar', str(today_year), str(today_month))

    # return render(request, "ees_forms/scheduling.html", {
    #     'options': options, 'facility': facility, 'today_year': today_year, 'today_month': today_month, 'supervisor': supervisor,
    # })

@lock
def event_add_view(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    companyData = request.user.user_profile.company
    listOfObservers = user_profile_model.objects.filter(company__id=companyData.id, position='observer')
    today = datetime.now().date()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    form_var = events_form()
    fullName = request.user.first_name + " " + request.user.last_name


    facilities = getCompanyFacilities(request.user.user_profile.company.company_name)
    userCalendars = request.user.user_profile.settings['calendar']['calendars']['default']
    cal_select_choices = [group['name'] for group in userCalendars] + [f.facility_name for f in facilities]


    if request.method == "POST":
        answer = request.POST
        request_form = events_form(request.POST)
        if request_form.is_valid():
            selected_days = request_form.cleaned_data['selected_days'].split(',')
            allDay = True if answer.get('allDay') else False
            calendarChoice = answer['calendarChoice']
            if facility == "supervisor":
                personal = True
            else:
                facilityChoice = facility
                personal = False

            for date in selected_days:
                clean_date = datetime.strptime(date.strip(), "%Y-%m-%d").date()
                Event.objects.create(
                    observer=answer['observer'],
                    title=answer['title'],
                    notes=answer['notes'],
                    start_time=answer['start_time'],
                    end_time=answer['end_time'],
                    date=clean_date,
                    userProf=request.user.user_profile,
                    calendarChoice=calendarChoice,
                    allDay=allDay,
                    facilityChoice=facilityChoice
                )

            cal_link = '../schedule/' + str(today_year) + '/' + today_month

            return redirect(cal_link)

    return render(request, "supervisor/event_add.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData,
        'facility': facility, 
        'today_year': today_year, 
        'today_month': today_month, 
        'form': form_var, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock, 
        'listOfObservers': listOfObservers,
        'cal_select_choices': cal_select_choices
    })

@lock
def event_detail_view(request, access_page, event_id):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    today = datetime.now().date()
    today_year = int(today.year)
    today_month = str(calendar.month_name[today.month])
    options = facility_model.objects.all()
    companyData = user_profile_model.objects.get(user__id=request.user.id).company
    listOfObservers = user_profile_model.objects.filter(company__id=companyData.id, position='observer')
    
    facilities = getCompanyFacilities(request.user.user_profile.company.company_name)
    userCalendars = request.user.user_profile.settings['calendar']['calendars']['default']
    cal_select_choices = [group['name'] for group in userCalendars] + [f.facility_name for f in facilities]

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
        print(data_pull.title)
        initial_data = {
            'title': data_pull.title,
            'date': data_pull.date,
            'start_time': data_pull.start_time,
            'end_time': data_pull.end_time,
            'notes': data_pull.notes,
            'allDay': data_pull.allDay,
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
        'listOfObservers': listOfObservers,
        'cal_select_choices': cal_select_choices
    })

@lock
@csrf_exempt
def delete_event(request, event_id):
    if request.method == "DELETE":
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'status': 'deleted'})
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)




