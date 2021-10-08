from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import user_profile_model, daily_battery_profile_model, formC_model, formC_readings_model, Forms
from ..forms import SubFormC1, FormCReadForm

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formC(request, selector):
    formName = "C"
    now = datetime.datetime.now()
    existing = False
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    count_bp = daily_battery_profile_model.objects.count()
    full_name = request.user.get_full_name()
    org = formC_model.objects.all().order_by('-date')
    org2 = formC_readings_model.objects.all().order_by('-form')

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
        if existing:
            initial_data = {
                'date': database_form.date,
                'truck_sel': database_form.truck_sel,
                'area_sel': database_form.area_sel,
                'truck_start_time': database_form.truck_start_time,
                'truck_stop_time': database_form.truck_stop_time,
                'area_start_time': database_form.area_start_time,
                'area_stop_time': database_form.area_stop_time,
                'observer': database_form.observer,
                'cert_date': database_form.cert_date,
                'comments': database_form.comments,
                'average_t': database_form.average_t,
                'average_p': database_form.average_p,

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

                if B.form.average_t > 5:
                    issue_page = '../../issues_view/C/' + str(database_form.date) + '/form'

                    return redirect(issue_page)
                if B.form.average_p > 5:
                    issue_page = '../../issues_view/C/' + str(database_form.date) + '/form'

                    return redirect(issue_page)

                if A.comments not in {'-', 'n/a', 'N/A'}:
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
        'form': form, 'read': read, "back": back, 'profile': profile, 'selector': selector, 'formName': formName
    })
