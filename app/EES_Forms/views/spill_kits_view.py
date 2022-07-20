from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import spill_kits_form
from ..models import daily_battery_profile_model, Forms, spill_kits_model
import datetime

lock = login_required(login_url='Login')


@lock
def spill_kits(request, access_page):
    formName = "SpillKits"
    existing = False
    unlock = False
    client = False
    search = False
    admin = False
    if request.user.groups.filter(name='SGI Technician'):
        unlock = True
    if request.user.groups.filter(name='EES Coke Employees'):
        client = True
    if request.user.groups.filter(name='SGI Admin') or request.user.is_superuser:
        admin = True
        
    now = datetime.datetime.now()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    sk_form = spill_kits_form
    
    count_bp = daily_battery_profile_model.objects.count()

    org = spill_kits_model.objects.all().order_by('-date')
    
    if count_bp != 0:
        todays_log = daily_prof[0]
        if access_page != 'form':
                for x in org:
                    if str(x.date) == str(access_page):
                        database_model = x
                data = database_model

                existing = True
                search = True
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
        'sk_form': sk_form, 'selector': access_page, 'admin': admin, "client": client, 'unlock': unlock
    })
