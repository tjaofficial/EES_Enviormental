from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import spill_kits_form
from ..models import daily_battery_profile_model, Forms
import datetime

lock = login_required(login_url='Login')
now = datetime.datetime.now()


@lock
def spill_kits(request, access_page):
    sk_form = spill_kits_form
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        if request.method == "POST":
            form = spill_kits_form(request.POST)
            if form.is_valid():
                form.save()

                done = Forms.objects.filter(form='spill_kits')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, 'Monthly/spillkits.html', {
        'sk_form': sk_form,
    })
