from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formM_model
import calendar

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formN(request, selector):
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    month_name = calendar.month_name[today.month]
    form_pull = formM_model.objects.all()
    count_bp = daily_battery_profile_model.objects.count()

    paved_loc = []
    for x in form_pull:
        if x.paved:
            if x.date.month == today.month:
                paved_loc.append((x.paved, x.date))
    
    unpaved_loc = []
    for x in form_pull:
        if x.unpaved:
            if x.date.month == today.month:
                unpaved_loc.append((x.unpaved, x.date))
                
    parking_loc = []
    for x in form_pull:
        if x.parking:
            if x.date.month == today.month:
                parking_loc.append((x.parking, x.date))
                
    storage_loc = []
    for x in form_pull:
        if x.storage:
            if x.date.month == today.month:
                storage_loc.append((x.storage, x.date))

    if count_bp != 0:
        todays_log = daily_prof[0]
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Monthly/formn.html", {
        'now': todays_log, 'selector': selector, 'profile': profile, 'month_name': month_name, 'paved_loc': paved_loc, 'unpaved_loc': unpaved_loc, 'parking_loc': parking_loc, 'storage_loc': storage_loc,
    })
