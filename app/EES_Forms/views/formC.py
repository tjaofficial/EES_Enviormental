from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import issues_model, user_profile_model, daily_battery_profile_model, formC_model, formC_readings_model, Forms
from ..forms import SubFormC1, FormCReadForm

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formC(request, selector):
    formName = "C"
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
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    
    org = formC_model.objects.all().order_by('-date')
    org2 = formC_readings_model.objects.all().order_by('-form')
    
    count_bp = daily_battery_profile_model.objects.count()
    
    full_name = request.user.get_full_name()
    

    if len(profile) > 0:
        same_user = user_profile_model.objects.filter(user__exact=request.user.id)
        if same_user:
            cert_date = request.user.user_profile_model.cert_date
        else:
            return redirect('IncompleteForms')
    else:
        return redirect('IncompleteForms')

    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            form = database_model
            for x in org2:
                if str(x.form.date) == str(selector):
                    database_model2 = x
            read = database_model2
            existing = True
            search = True
        # ------check if database is empty----------
        elif len(org) > 0 or len(org2) > 0:
            database_form = org[0]
            database_form2 = org2[0]
            # -------check if there is a daily battery profile
            if now.month == todays_log.date_save.month:
                if now.day == todays_log.date_save.day:
                    if todays_log.date_save == database_form.date:
                        existing = True
                else:
                    batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                    return redirect(batt_prof)
            else:
                batt_prof = '../../daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

                return redirect(batt_prof)
            
        if search:
            database_form = ''
        else:
            if existing:
                initial_data = {
                    'date': database_form.date,
                    'truck_sel': database_form.truck_sel,
                    'area_sel': database_form.area_sel,
                    'truck_start_time': database_form.truck_start_time,
                    'truck_stop_time': database_form.truck_stop_time,
                    'area_start_time': database_form.area_start_time,
                    'area_stop_time': database_form.area_stop_time,
                    'sto_start_time': database_form.sto_start_time,
                    'sto_stop_time': database_form.sto_stop_time,
                    'salt_start_time': database_form.salt_start_time,
                    'salt_stop_time': database_form.salt_stop_time,
                    'observer': database_form.observer,
                    'cert_date': database_form.cert_date,
                    'comments': database_form.comments,
                    'average_t': database_form.average_t,
                    'average_p': database_form.average_p,
                    'average_storage': database_form.average_storage,
                    'average_salt': database_form.average_salt,

                    'TRead1': database_form2.TRead1,
                    'TRead2': database_form2.TRead2,
                    'TRead3': database_form2.TRead3,
                    'TRead4': database_form2.TRead4,
                    'TRead5': database_form2.TRead5,
                    'TRead6': database_form2.TRead6,
                    'TRead7': database_form2.TRead7,
                    'TRead8': database_form2.TRead8,
                    'TRead9': database_form2.TRead9,
                    'TRead10': database_form2.TRead10,
                    'TRead11': database_form2.TRead11,
                    'TRead12': database_form2.TRead12,
                    'ARead1': database_form2.ARead1,
                    'ARead2': database_form2.ARead2,
                    'ARead3': database_form2.ARead3,
                    'ARead4': database_form2.ARead4,
                    'ARead5': database_form2.ARead5,
                    'ARead6': database_form2.ARead6,
                    'ARead7': database_form2.ARead7,
                    'ARead8': database_form2.ARead8,
                    'ARead9': database_form2.ARead9,
                    'ARead10': database_form2.ARead10,
                    'ARead11': database_form2.ARead11,
                    'ARead12': database_form2.ARead12,
                    'storage_1': database_form2.storage_1,
                    'storage_2': database_form2.storage_2,
                    'storage_3': database_form2.storage_3,
                    'storage_4': database_form2.storage_4,
                    'storage_5': database_form2.storage_5,
                    'storage_6': database_form2.storage_6,
                    'storage_7': database_form2.storage_7,
                    'storage_8': database_form2.storage_8,
                    'storage_9': database_form2.storage_9,
                    'storage_10': database_form2.storage_10,
                    'storage_11': database_form2.storage_11,
                    'storage_12': database_form2.storage_12,
                    'salt_1': database_form2.salt_1,
                    'salt_2': database_form2.salt_2,
                    'salt_3': database_form2.salt_3,
                    'salt_4': database_form2.salt_4,
                    'salt_5': database_form2.salt_5,
                    'salt_6': database_form2.salt_6,
                    'salt_7': database_form2.salt_7,
                    'salt_8': database_form2.salt_8,
                    'salt_9': database_form2.salt_9,
                    'salt_10': database_form2.salt_10,
                    'salt_11': database_form2.salt_11,
                    'salt_12': database_form2.salt_12,
                }
                read = FormCReadForm(initial=initial_data)
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'cert_date': cert_date,
                }
                read = FormCReadForm()

            form = SubFormC1(initial=initial_data)
        if request.method == "POST":
            if existing:
                CData = SubFormC1(request.POST, instance=database_form)
                CReadings = FormCReadForm(request.POST, instance=database_form2)
            else:
                CReadings = FormCReadForm(request.POST)
                CData = SubFormC1(request.POST)

            
            A_valid = CReadings.is_valid()
            B_valid = CData.is_valid()

            if A_valid and B_valid:
                A = CData.save()
                B = CReadings.save(commit=False)
                B.form = A
                B.save()

                if B.form.average_t > 5 or B.form.average_p > 5 or A.comments not in {'-', 'n/a', 'N/A'}:
                    finder = issues_model.objects.filter(date=A.date, form='C')
                    if finder:
                        issue_page = '../../issues_view/C/' + str(database_form.date) + '/issue'
                    else:
                        issue_page = '../../issues_view/C/' + str(database_form.date) + '/form'

                    return redirect(issue_page)

                done = Forms.objects.filter(form='C')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formC.html", {
        "client": client, 'unlock': unlock, 'admin': admin, 'form': form, 'read': read, "back": back, 'profile': profile, 'selector': selector, 'formName': formName
    })
