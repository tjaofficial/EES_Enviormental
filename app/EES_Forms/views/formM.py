from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formM_model, formM_readings_model
from ..forms import formM_form, formM_readings_form

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formM(request, selector):
    formName = "M"
    existing = False
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    today = datetime.date.today()
    today_number = today.weekday()
    count_bp = daily_battery_profile_model.objects.count()
    org = formM_model.objects.all().order_by('-date')
    org2 = formM_readings_model.objects.all().order_by('-form')

    if count_bp != 0:
        todays_log = daily_prof[0]
        if selector != 'form':
            for x in org:
                if str(x.date) == str(selector):
                    database_model = x
            form = database_model
        if selector != 'form':
            for x in org2:
                if str(x.form) == str(selector):
                    database_model2 = x
                else:
                    print('Error - EES_00001')
            form2 = database_model2
        elif len(org) > 0 or len(org2) > 0:
            database_form = org[0]
            database_form2 = org2[0]
            if selector == 'form':
                if today_number in {0, 1, 2, 3, 4}:
                    if todays_log.date_save == database_form.date:
                        existing = True
        if existing:
            initial_data = {
                'date': database_form.date,
                'paved': database_form.paved,
                'pav_start': database_form.pav_start,
                'pav_stop': database_form.pav_stop,
                'unpaved': database_form.unpaved,
                'unp_start': database_form.unp_start,
                'unp_stop': database_form.unp_stop,
                'parking': database_form.parking,
                'par_start': database_form.par_start,
                'par_stop': database_form.par_stop,
                'observer': database_form.observer,
                'cert_date': database_form.cert_date,
                'comments': database_form.comments,

                'pav_1': database_form2.pav_1,
                'pav_2': database_form2.pav_2,
                'pav_3': database_form2.pav_3,
                'pav_4': database_form2.pav_4,
                'pav_5': database_form2.pav_5,
                'pav_6': database_form2.pav_6,
                'pav_7': database_form2.pav_7,
                'pav_8': database_form2.pav_8,
                'pav_9': database_form2.pav_9,
                'pav_10': database_form2.pav_10,
                'pav_11': database_form2.pav_11,
                'pav_12': database_form2.pav_12,
                'unp_1': database_form2.unp_1,
                'unp_2': database_form2.unp_2,
                'unp_3': database_form2.unp_3,
                'unp_4': database_form2.unp_4,
                'unp_5': database_form2.unp_5,
                'unp_6': database_form2.unp_6,
                'unp_7': database_form2.unp_7,
                'unp_8': database_form2.unp_8,
                'unp_9': database_form2.unp_9,
                'unp_10': database_form2.unp_10,
                'unp_11': database_form2.unp_11,
                'unp_12': database_form2.unp_12,
                'par_1': database_form2.par_1,
                'par_2': database_form2.par_2,
                'par_3': database_form2.par_3,
                'par_4': database_form2.par_4,
                'par_5': database_form2.par_5,
                'par_6': database_form2.par_6,
                'par_7': database_form2.par_7,
                'par_8': database_form2.par_8,
                'par_9': database_form2.par_9,
                'par_10': database_form2.par_10,
                'par_11': database_form2.par_11,
                'par_12': database_form2.par_12,

                'pav_total': database_form2.pav_total,
                'unp_total': database_form2.unp_total,
                'par_total': database_form2.par_total,
            }
            form2 = formM_readings_form(initial=initial_data)
        else:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name,
                'cert_date': cert_date
            }
            form2 = formM_readings_form()

        form = formM_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formM_form(request.POST, instance=database_form)
                reads = formM_readings_form(request.POST, instance=database_form2)
            else:
                form = formM_form(request.POST)
                reads = formM_readings_form(request.POST)

            A_valid = form.is_valid()
            B_valid = reads.is_valid()

            if A_valid and B_valid:
                A = form.save()
                B = reads.save(commit=False)
                B.form = A
                B.save()

                done = Forms.objects.filter(form='M')[0]
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()

                done2 = Forms.objects.filter(form='N')[0]
                done2.submitted = True
                done2.date_submitted = todays_log.date_save
                done2.save()

                return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Daily/formM.html", {
        'now': todays_log, 'form': form, 'selector': selector, 'profile': profile, 'read': form2, 'formName': formName,
    })
