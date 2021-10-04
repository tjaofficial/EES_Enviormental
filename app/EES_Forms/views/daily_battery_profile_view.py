from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import daily_battery_profile_model, user_profile_model
from ..forms import daily_battery_profile_form

lock = login_required(login_url='Login')
now = datetime.datetime.now()
profile = user_profile_model.objects.all()


@lock
def daily_battery_profile_view(request, access_page, date):
    profile = user_profile_model.objects.all()
    form = daily_battery_profile_form

    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    existing = False
    todays_log = ''

    if len(daily_prof) > 0:
        todays_log = daily_prof[0]
        if now.month == todays_log.date_save.month:
            if now.day == todays_log.date_save.day:
                existing = True
                initial_data = {
                    'foreman': todays_log.foreman,
                    'crew': todays_log.crew,
                    'inop_ovens': todays_log.inop_ovens,
                    'date_save': todays_log.date_save,
                }
                form = daily_battery_profile_form(initial=initial_data)

    if request.method == 'POST':
        if existing:
            form = daily_battery_profile_form(request.POST, instance=todays_log)
        else:
            form = daily_battery_profile_form(request.POST)
        if form.is_valid():
            form.save()

            return redirect('IncompleteForms')

    return render(request, "ees_forms/Bat_Info.html", {
        'form': form, 'now': now, 'todays_log': todays_log, 'profile': profile
    })
