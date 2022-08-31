from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import spill_kits_form
from ..models import daily_battery_profile_model, Forms, spill_kits_model
import datetime
import calendar

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
    sk_form = spill_kits_form()
    full_name = request.user.get_full_name()
    count_bp = daily_battery_profile_model.objects.count()
    today = datetime.date.today()
    org = spill_kits_model.objects.all().order_by('-date')
    
    month_name = calendar.month_name[today.month]
    
    if count_bp != 0:
        todays_log = daily_prof[0]
        if access_page != 'form':
            print('CHECK 1')
            for x in org:
                if str(x.date) == str(access_page):
                    database_model = x
            data = database_model

            existing = True
            search = True
        elif len(org) > 0:
            print('CHECK 2')
            database_form = org[0]
            datetime_object = datetime.datetime.strptime(database_form.month, "%B")
            month_number = datetime_object.month

            if now.month == month_number:
                print('CHECK 3')
                existing = True

        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'observer': database_form.observer,
                    'date': database_form.date,
                    'month': database_form.month,
                    'sk1_tag_on': database_form.sk1_tag_on,
                    'sk1_serial': database_form.sk1_serial,
                    'sk1_complete': database_form.sk1_complete,
                    'sk1_report': database_form.sk1_report,
                    'sk1_comment': database_form.sk1_comment,
                    
                    'sk2_tag_on': database_form.sk2_tag_on,
                    'sk2_serial': database_form.sk2_serial,
                    'sk2_complete': database_form.sk2_complete,
                    'sk2_report': database_form.sk2_report,
                    'sk2_comment': database_form.sk2_comment,
                    
                    'sk3_tag_on': database_form.sk3_tag_on,
                    'sk3_serial': database_form.sk3_serial,
                    'sk3_complete': database_form.sk3_complete,
                    'sk3_report': database_form.sk3_report,
                    'sk3_comment': database_form.sk3_comment,
                    
                    'sk4_tag_on': database_form.sk4_tag_on,
                    'sk4_serial': database_form.sk4_serial,
                    'sk4_complete': database_form.sk4_complete,
                    'sk4_report': database_form.sk4_report,
                    'sk4_comment': database_form.sk4_comment,
                    
                    'sk5_tag_on': database_form.sk5_tag_on,
                    'sk5_serial': database_form.sk5_serial,
                    'sk5_complete': database_form.sk5_complete,
                    'sk5_report': database_form.sk5_report,
                    'sk5_comment': database_form.sk5_comment,
                    
                    'sk6_tag_on': database_form.sk6_tag_on,
                    'sk6_serial': database_form.sk6_serial,
                    'sk6_complete': database_form.sk6_complete,
                    'sk6_report': database_form.sk6_report,
                    'sk6_comment': database_form.sk6_comment,
                    
                    'sk7_tag_on': database_form.sk7_tag_on,
                    'sk7_serial': database_form.sk7_serial,
                    'sk7_complete': database_form.sk7_complete,
                    'sk7_report': database_form.sk7_report,
                    'sk7_comment': database_form.sk7_comment,
                    
                    'sk8_tag_on': database_form.sk8_tag_on,
                    'sk8_serial': database_form.sk8_serial,
                    'sk8_complete': database_form.sk8_complete,
                    'sk8_report': database_form.sk8_report,
                    'sk8_comment': database_form.sk8_comment,
                    
                    'sk9_tag_on': database_form.sk9_tag_on,
                    'sk9_serial': database_form.sk9_serial,
                    'sk9_complete': database_form.sk9_complete,
                    'sk9_report': database_form.sk9_report,
                    'sk9_comment': database_form.sk9_comment,
                    
                    'sk10_tag_on': database_form.sk10_tag_on,
                    'sk10_serial': database_form.sk10_serial,
                    'sk10_complete': database_form.sk10_complete,
                    'sk10_report': database_form.sk10_report,
                    'sk10_comment': database_form.sk10_comment,
                    
                    'sk11_tag_on': database_form.sk1_tag_on,
                    'sk11_serial': database_form.sk1_serial,
                    'sk11_complete': database_form.sk1_complete,
                    'sk11_report': database_form.sk1_report,
                    'sk11_comment': database_form.sk1_comment,
                    
                    'sk12_tag_on': database_form.sk2_tag_on,
                    'sk12_serial': database_form.sk2_serial,
                    'sk12_complete': database_form.sk2_complete,
                    'sk12_report': database_form.sk2_report,
                    'sk12_comment': database_form.sk2_comment,
                    
                    'sk13_tag_on': database_form.sk3_tag_on,
                    'sk13_serial': database_form.sk3_serial,
                    'sk13_complete': database_form.sk3_complete,
                    'sk13_report': database_form.sk3_report,
                    'sk13_comment': database_form.sk3_comment,
                    
                    'sk14_tag_on': database_form.sk4_tag_on,
                    'sk14_serial': database_form.sk4_serial,
                    'sk14_complete': database_form.sk4_complete,
                    'sk14_report': database_form.sk4_report,
                    'sk14_comment': database_form.sk4_comment,
                    
                    'sk15_tag_on': database_form.sk5_tag_on,
                    'sk15_serial': database_form.sk5_serial,
                    'sk15_complete': database_form.sk5_complete,
                    'sk15_report': database_form.sk5_report,
                    'sk15_comment': database_form.sk5_comment,
                    
                    'sk16_tag_on': database_form.sk6_tag_on,
                    'sk16_serial': database_form.sk6_serial,
                    'sk16_complete': database_form.sk6_complete,
                    'sk16_report': database_form.sk6_report,
                    'sk16_comment': database_form.sk6_comment,
                    
                    'sk17_tag_on': database_form.sk7_tag_on,
                    'sk17_serial': database_form.sk7_serial,
                    'sk17_complete': database_form.sk7_complete,
                    'sk17_report': database_form.sk7_report,
                    'sk17_comment': database_form.sk7_comment,
                    
                    'sk18_tag_on': database_form.sk8_tag_on,
                    'sk18_serial': database_form.sk8_serial,
                    'sk18_complete': database_form.sk8_complete,
                    'sk18_report': database_form.sk8_report,
                    'sk18_comment': database_form.sk8_comment,
                    
                    'sk19_tag_on': database_form.sk9_tag_on,
                    'sk19_serial': database_form.sk9_serial,
                    'sk19_complete': database_form.sk9_complete,
                    'sk19_report': database_form.sk9_report,
                    'sk19_comment': database_form.sk9_comment,
                    
                    'sk20_tag_on': database_form.sk10_tag_on,
                    'sk20_serial': database_form.sk10_serial,
                    'sk20_complete': database_form.sk10_complete,
                    'sk20_report': database_form.sk10_report,
                    'sk20_comment': database_form.sk10_comment,
                    
                    'sk21_tag_on': database_form.sk1_tag_on,
                    'sk21_serial': database_form.sk1_serial,
                    'sk21_complete': database_form.sk1_complete,
                    'sk21_report': database_form.sk1_report,
                    'sk21_comment': database_form.sk1_comment,
                    
                    'sk22_tag_on': database_form.sk2_tag_on,
                    'sk22_serial': database_form.sk2_serial,
                    'sk22_complete': database_form.sk2_complete,
                    'sk22_report': database_form.sk2_report,
                    'sk22_comment': database_form.sk2_comment,
                    
                    'sk23_tag_on': database_form.sk3_tag_on,
                    'sk23_serial': database_form.sk3_serial,
                    'sk23_complete': database_form.sk3_complete,
                    'sk23_report': database_form.sk3_report,
                    'sk23_comment': database_form.sk3_comment,
                    
                    'sk24_tag_on': database_form.sk4_tag_on,
                    'sk24_serial': database_form.sk4_serial,
                    'sk24_complete': database_form.sk4_complete,
                    'sk24_report': database_form.sk4_report,
                    'sk24_comment': database_form.sk4_comment,
                    
                    'sk25_tag_on': database_form.sk5_tag_on,
                    'sk25_serial': database_form.sk5_serial,
                    'sk25_complete': database_form.sk5_complete,
                    'sk25_report': database_form.sk5_report,
                    'sk25_comment': database_form.sk5_comment,
                    
                    'sk26_tag_on': database_form.sk6_tag_on,
                    'sk26_serial': database_form.sk6_serial,
                    'sk26_complete': database_form.sk6_complete,
                    'sk26_report': database_form.sk6_report,
                    'sk26_comment': database_form.sk6_comment,
                    
                    'sk27_tag_on': database_form.sk7_tag_on,
                    'sk27_serial': database_form.sk7_serial,
                    'sk27_complete': database_form.sk7_complete,
                    'sk27_report': database_form.sk7_report,
                    'sk27_comment': database_form.sk7_comment,
                }
            else:
                initial_data = {
                    'observer': full_name,
                    'date': todays_log.date_save,
                    'month': month_name,
                }
            data = spill_kits_form(initial=initial_data)
        
        if request.method == "POST":
            if existing:
                form = spill_kits_form(request.POST, instance=database_form)
            else:
                form = spill_kits_form(request.POST)
                
            if form.is_valid():
                form.save()

                done = Forms.objects.filter(form='Spill Kits')[0]
                print(done.submitted)
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, 'Monthly/spillkits.html', {
        'sk_form': data, 'selector': access_page, 'admin': admin, "client": client, 'unlock': unlock, 'formName': formName
    })
