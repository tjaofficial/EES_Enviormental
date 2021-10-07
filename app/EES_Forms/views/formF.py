from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formF1_model, formF2_model, formF3_model, formF4_model, formF5_model, formF6_model, formF7_model
from ..forms import formF1_form, formF2_form, formF3_form, formF4_form, formF5_form, formF6_form, formF7_form
from dateutil.relativedelta import relativedelta

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formF1(request, selector):
    formName = "F1"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    form_all = formF1_model.objects.count()

    full_name = request.user.get_full_name()
    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        if form_all == 0:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name,
                'retain_date': todays_log.date_save + relativedelta(years=5)
            }
            data = formF1_form(initial=initial_data)
            if request.method == "POST":
                form = formF1_form(request.POST)
                if form.is_valid():

                    form.save()

                    done = Forms.objects.filter(form='F-1')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')

        else:
            if today.weekday() not in {0, 1, 5, 6}:
                org = formF1_model.objects.all().order_by('-date')
                database_form = org[0]
                if today.weekday() == 2:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'observer': database_form.observer,
                            'time': database_form.time,
                            'date': database_form.date,
                            'retain_date': database_form.retain_date,
                            'status_1': database_form.status_1,
                            'status_2': database_form.status_2,
                            'status_3': database_form.status_3,
                            'status_4': database_form.status_4,
                            'status_5': database_form.status_5,
                            'status_6': database_form.status_6,
                            'status_7': database_form.status_7,
                            'comments_1': database_form.comments_1,
                            'comments_2': database_form.comments_2,
                            'comments_3': database_form.comments_3,
                            'comments_4': database_form.comments_4,
                            'comments_5': database_form.comments_5,
                            'comments_6': database_form.comments_6,
                            'comments_7': database_form.comments_7,
                            'action_1': database_form.action_1,
                            'action_2': database_form.action_2,
                            'action_3': database_form.action_3,
                            'action_4': database_form.action_4,
                            'action_5': database_form.action_5,
                            'action_6': database_form.action_6,
                            'action_7': database_form.action_7,
                            'waste_des_1': database_form.waste_des_1,
                            'waste_des_2': database_form.waste_des_2,
                            'waste_des_3': database_form.waste_des_3,
                            'waste_des_4': database_form.waste_des_4,
                            'containers_1': database_form.containers_1,
                            'containers_2': database_form.containers_2,
                            'containers_3': database_form.containers_3,
                            'containers_4': database_form.containers_4,
                            'waste_codes_1': database_form.waste_codes_1,
                            'waste_codes_2': database_form.waste_codes_2,
                            'waste_codes_3': database_form.waste_codes_3,
                            'waste_codes_4': database_form.waste_codes_4,
                            'dates_1': database_form.dates_1,
                            'dates_2': database_form.dates_2,
                            'dates_3': database_form.dates_3,
                            'dates_4': database_form.dates_4,
                        }
                        data = formF1_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF1_form(request.POST, instance=database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-1')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name,
                            'retain_date': todays_log.date_save + relativedelta(years=5)
                        }
                        data = formF1_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF1_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-1')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    if today.weekday() in {3, 4}:
                        last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                        if last_wed == database_form.date:
                            initial_data = {
                                'observer': database_form.observer,
                                'time': database_form.time,
                                'date': database_form.date,
                                'retain_date': database_form.retain_date,
                                'status_1': database_form.status_1,
                                'status_2': database_form.status_2,
                                'status_3': database_form.status_3,
                                'status_4': database_form.status_4,
                                'status_5': database_form.status_5,
                                'status_6': database_form.status_6,
                                'status_7': database_form.status_7,
                                'comments_1': database_form.comments_1,
                                'comments_2': database_form.comments_2,
                                'comments_3': database_form.comments_3,
                                'comments_4': database_form.comments_4,
                                'comments_5': database_form.comments_5,
                                'comments_6': database_form.comments_6,
                                'comments_7': database_form.comments_7,
                                'action_1': database_form.action_1,
                                'action_2': database_form.action_2,
                                'action_3': database_form.action_3,
                                'action_4': database_form.action_4,
                                'action_5': database_form.action_5,
                                'action_6': database_form.action_6,
                                'action_7': database_form.action_7,
                                'waste_des_1': database_form.waste_des_1,
                                'waste_des_2': database_form.waste_des_2,
                                'waste_des_3': database_form.waste_des_3,
                                'waste_des_4': database_form.waste_des_4,
                                'containers_1': database_form.containers_1,
                                'containers_2': database_form.containers_2,
                                'containers_3': database_form.containers_3,
                                'containers_4': database_form.containers_4,
                                'waste_codes_1': database_form.waste_codes_1,
                                'waste_codes_2': database_form.waste_codes_2,
                                'waste_codes_3': database_form.waste_codes_3,
                                'waste_codes_4': database_form.waste_codes_4,
                                'dates_1': database_form.dates_1,
                                'dates_2': database_form.dates_2,
                                'dates_3': database_form.dates_3,
                                'dates_4': database_form.dates_4,
                            }
                            data = formF1_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF1_form(request.POST, instance=database_form)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-1')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'date': todays_log.date_save,
                                'observer': full_name,
                                'retain_date': todays_log.date_save + relativedelta(years=5)
                            }
                            data = formF1_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF1_form(request.POST)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-1')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name,
                    'retain_date': todays_log.date_save + relativedelta(years=5)
                }
                data = formF1_form(initial=initial_data)
                if request.method == "POST":
                    form = formF1_form(request.POST)
                    if form.is_valid():
                        form.save()

                        done = Forms.objects.filter(form='F-1')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formF1.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector': selector, 'profile': profile, 'formName': formName
    })


@lock
def formF2(request, selector):
    formName = "F2"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    form_all = formF2_model.objects.count()

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        if form_all == 0:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name
            }
            data = formF2_form(initial=initial_data)
            if request.method == "POST":
                form = formF2_form(request.POST)
                if form.is_valid():

                    form.save()

                    done = Forms.objects.filter(form='F-2')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')

        else:
            if today.weekday() not in {0, 1, 5, 6}:
                org = formF2_model.objects.all().order_by('-date')
                database_form = org[0]
                if today.weekday() == 2:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'observer': database_form.observer,
                            'time': database_form.time,
                            'date': database_form.date,
                            'retain_date': database_form.retain_date,
                            'status_1': database_form.status_1,
                            'status_2': database_form.status_2,
                            'status_3': database_form.status_3,
                            'status_4': database_form.status_4,
                            'status_5': database_form.status_5,
                            'status_6': database_form.status_6,
                            'status_7': database_form.status_7,
                            'comments_1': database_form.comments_1,
                            'comments_2': database_form.comments_2,
                            'comments_3': database_form.comments_3,
                            'comments_4': database_form.comments_4,
                            'comments_5': database_form.comments_5,
                            'comments_6': database_form.comments_6,
                            'comments_7': database_form.comments_7,
                            'action_1': database_form.action_1,
                            'action_2': database_form.action_2,
                            'action_3': database_form.action_3,
                            'action_4': database_form.action_4,
                            'action_5': database_form.action_5,
                            'action_6': database_form.action_6,
                            'action_7': database_form.action_7,
                            'waste_des_1': database_form.waste_des_1,
                            'waste_des_2': database_form.waste_des_2,
                            'waste_des_3': database_form.waste_des_3,
                            'waste_des_4': database_form.waste_des_4,
                            'containers_1': database_form.containers_1,
                            'containers_2': database_form.containers_2,
                            'containers_3': database_form.containers_3,
                            'containers_4': database_form.containers_4,
                            'waste_codes_1': database_form.waste_codes_1,
                            'waste_codes_2': database_form.waste_codes_2,
                            'waste_codes_3': database_form.waste_codes_3,
                            'waste_codes_4': database_form.waste_codes_4,
                            'dates_1': database_form.dates_1,
                            'dates_2': database_form.dates_2,
                            'dates_3': database_form.dates_3,
                            'dates_4': database_form.dates_4,
                        }
                        data = formF2_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF2_form(request.POST, instance=database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-2')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name
                        }
                        data = formF2_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF2_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-2')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    if today.weekday() in {3, 4}:
                        last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                        if last_wed == database_form.date:
                            initial_data = {
                                'observer': database_form.observer,
                                'time': database_form.time,
                                'date': database_form.date,
                                'retain_date': database_form.retain_date,
                                'status_1': database_form.status_1,
                                'status_2': database_form.status_2,
                                'status_3': database_form.status_3,
                                'status_4': database_form.status_4,
                                'status_5': database_form.status_5,
                                'status_6': database_form.status_6,
                                'comments_1': database_form.comments_1,
                                'comments_2': database_form.comments_2,
                                'comments_3': database_form.comments_3,
                                'comments_4': database_form.comments_4,
                                'comments_5': database_form.comments_5,
                                'comments_6': database_form.comments_6,
                                'action_1': database_form.action_1,
                                'action_2': database_form.action_2,
                                'action_3': database_form.action_3,
                                'action_4': database_form.action_4,
                                'action_5': database_form.action_5,
                                'action_6': database_form.action_6,
                                'waste_des_1': database_form.waste_des_1,
                                'waste_des_2': database_form.waste_des_2,
                                'waste_des_3': database_form.waste_des_3,
                                'waste_des_4': database_form.waste_des_4,
                                'containers_1': database_form.containers_1,
                                'containers_2': database_form.containers_2,
                                'containers_3': database_form.containers_3,
                                'containers_4': database_form.containers_4,
                                'waste_codes_1': database_form.waste_codes_1,
                                'waste_codes_2': database_form.waste_codes_2,
                                'waste_codes_3': database_form.waste_codes_3,
                                'waste_codes_4': database_form.waste_codes_4,
                                'dates_1': database_form.dates_1,
                                'dates_2': database_form.dates_2,
                                'dates_3': database_form.dates_3,
                                'dates_4': database_form.dates_4,
                            }
                            data = formF2_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF2_form(request.POST, instance=database_form)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-2')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'date': todays_log.date_save,
                                'observer': full_name
                            }
                            data = formF2_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF2_form(request.POST)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-2')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name
                }
                data = formF2_form(initial=initial_data)
                if request.method == "POST":
                    form = formF2_form(request.POST)
                    if form.is_valid():
                        form.save()

                        done = Forms.objects.filter(form='F-2')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formF2.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector': selector, 'profile': profile, 'formName': formName
    })


@lock
def formF3(request, selector):
    formName = "F3"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    form_all = formF3_model.objects.count()

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if form_all == 0:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name
            }
            data = formF3_form(initial=initial_data)
            if request.method == "POST":
                form = formF3_form(request.POST)
                if form.is_valid():

                    form.save()

                    done = Forms.objects.filter(form='F-3')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')

        else:
            if today.weekday() not in {0, 1, 5, 6}:
                org = formF3_model.objects.all().order_by('-date')
                database_form = org[0]
                if today.weekday() == 2:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'observer': database_form.observer,
                            'time': database_form.time,
                            'date': database_form.date,
                            'retain_date': database_form.retain_date,
                            'status_1': database_form.status_1,
                            'status_2': database_form.status_2,
                            'status_3': database_form.status_3,
                            'status_4': database_form.status_4,
                            'status_5': database_form.status_5,
                            'status_6': database_form.status_6,
                            'status_7': database_form.status_7,
                            'comments_1': database_form.comments_1,
                            'comments_2': database_form.comments_2,
                            'comments_3': database_form.comments_3,
                            'comments_4': database_form.comments_4,
                            'comments_5': database_form.comments_5,
                            'comments_6': database_form.comments_6,
                            'comments_7': database_form.comments_7,
                            'action_1': database_form.action_1,
                            'action_2': database_form.action_2,
                            'action_3': database_form.action_3,
                            'action_4': database_form.action_4,
                            'action_5': database_form.action_5,
                            'action_6': database_form.action_6,
                            'action_7': database_form.action_7,
                            'waste_des_1': database_form.waste_des_1,
                            'waste_des_2': database_form.waste_des_2,
                            'waste_des_3': database_form.waste_des_3,
                            'waste_des_4': database_form.waste_des_4,
                            'containers_1': database_form.containers_1,
                            'containers_2': database_form.containers_2,
                            'containers_3': database_form.containers_3,
                            'containers_4': database_form.containers_4,
                            'waste_codes_1': database_form.waste_codes_1,
                            'waste_codes_2': database_form.waste_codes_2,
                            'waste_codes_3': database_form.waste_codes_3,
                            'waste_codes_4': database_form.waste_codes_4,
                            'dates_1': database_form.dates_1,
                            'dates_2': database_form.dates_2,
                            'dates_3': database_form.dates_3,
                            'dates_4': database_form.dates_4,
                        }
                        data = formF3_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF3_form(request.POST, instance=database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-3')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name
                        }
                        data = formF3_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF3_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-3')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    if today.weekday() in {3, 4}:
                        last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                        if last_wed == database_form.date:
                            initial_data = {
                                'observer': database_form.observer,
                                'time': database_form.time,
                                'date': database_form.date,
                                'retain_date': database_form.retain_date,
                                'status_1': database_form.status_1,
                                'status_2': database_form.status_2,
                                'status_3': database_form.status_3,
                                'status_4': database_form.status_4,
                                'status_5': database_form.status_5,
                                'status_6': database_form.status_6,
                                'comments_1': database_form.comments_1,
                                'comments_2': database_form.comments_2,
                                'comments_3': database_form.comments_3,
                                'comments_4': database_form.comments_4,
                                'comments_5': database_form.comments_5,
                                'comments_6': database_form.comments_6,
                                'action_1': database_form.action_1,
                                'action_2': database_form.action_2,
                                'action_3': database_form.action_3,
                                'action_4': database_form.action_4,
                                'action_5': database_form.action_5,
                                'action_6': database_form.action_6,
                                'waste_des_1': database_form.waste_des_1,
                                'waste_des_2': database_form.waste_des_2,
                                'waste_des_3': database_form.waste_des_3,
                                'waste_des_4': database_form.waste_des_4,
                                'containers_1': database_form.containers_1,
                                'containers_2': database_form.containers_2,
                                'containers_3': database_form.containers_3,
                                'containers_4': database_form.containers_4,
                                'waste_codes_1': database_form.waste_codes_1,
                                'waste_codes_2': database_form.waste_codes_2,
                                'waste_codes_3': database_form.waste_codes_3,
                                'waste_codes_4': database_form.waste_codes_4,
                                'dates_1': database_form.dates_1,
                                'dates_2': database_form.dates_2,
                                'dates_3': database_form.dates_3,
                                'dates_4': database_form.dates_4,
                            }
                            data = formF3_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF3_form(request.POST, instance=database_form)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-3')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'date': todays_log.date_save,
                                'observer': full_name
                            }
                            data = formF3_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF3_form(request.POST)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-3')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name
                }
                data = formF3_form(initial=initial_data)
                if request.method == "POST":
                    form = formF3_form(request.POST)
                    if form.is_valid():
                        form.save()

                        done = Forms.objects.filter(form='F-3')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formF3.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector': selector, 'profile': profile, 'formName': formName
    })


@lock
def formF4(request, selector):
    formName = "F4"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    form_all = formF4_model.objects.count()

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if form_all == 0:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name
            }
            data = formF4_form(initial=initial_data)
            if request.method == "POST":
                form = formF4_form(request.POST)
                if form.is_valid():

                    form.save()

                    done = Forms.objects.filter(form='F-4')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')

        else:
            if today.weekday() not in {0, 1, 5, 6}:
                org = formF4_model.objects.all().order_by('-date')
                database_form = org[0]
                if today.weekday() == 2:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'observer': database_form.observer,
                            'time': database_form.time,
                            'date': database_form.date,
                            'retain_date': database_form.retain_date,
                            'status_1': database_form.status_1,
                            'status_2': database_form.status_2,
                            'status_3': database_form.status_3,
                            'status_4': database_form.status_4,
                            'status_5': database_form.status_5,
                            'status_6': database_form.status_6,
                            'status_7': database_form.status_7,
                            'comments_1': database_form.comments_1,
                            'comments_2': database_form.comments_2,
                            'comments_3': database_form.comments_3,
                            'comments_4': database_form.comments_4,
                            'comments_5': database_form.comments_5,
                            'comments_6': database_form.comments_6,
                            'comments_7': database_form.comments_7,
                            'action_1': database_form.action_1,
                            'action_2': database_form.action_2,
                            'action_3': database_form.action_3,
                            'action_4': database_form.action_4,
                            'action_5': database_form.action_5,
                            'action_6': database_form.action_6,
                            'action_7': database_form.action_7,
                            'waste_des_1': database_form.waste_des_1,
                            'waste_des_2': database_form.waste_des_2,
                            'waste_des_3': database_form.waste_des_3,
                            'waste_des_4': database_form.waste_des_4,
                            'containers_1': database_form.containers_1,
                            'containers_2': database_form.containers_2,
                            'containers_3': database_form.containers_3,
                            'containers_4': database_form.containers_4,
                            'waste_codes_1': database_form.waste_codes_1,
                            'waste_codes_2': database_form.waste_codes_2,
                            'waste_codes_3': database_form.waste_codes_3,
                            'waste_codes_4': database_form.waste_codes_4,
                            'dates_1': database_form.dates_1,
                            'dates_2': database_form.dates_2,
                            'dates_3': database_form.dates_3,
                            'dates_4': database_form.dates_4,
                        }
                        data = formF4_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF4_form(request.POST, instance=database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-4')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name
                        }
                        data = formF4_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF4_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-4')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    if today.weekday() in {3, 4}:
                        last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                        if last_wed == database_form.date:
                            initial_data = {
                                'observer': database_form.observer,
                                'time': database_form.time,
                                'date': database_form.date,
                                'retain_date': database_form.retain_date,
                                'status_1': database_form.status_1,
                                'status_2': database_form.status_2,
                                'status_3': database_form.status_3,
                                'status_4': database_form.status_4,
                                'status_5': database_form.status_5,
                                'status_6': database_form.status_6,
                                'comments_1': database_form.comments_1,
                                'comments_2': database_form.comments_2,
                                'comments_3': database_form.comments_3,
                                'comments_4': database_form.comments_4,
                                'comments_5': database_form.comments_5,
                                'comments_6': database_form.comments_6,
                                'action_1': database_form.action_1,
                                'action_2': database_form.action_2,
                                'action_3': database_form.action_3,
                                'action_4': database_form.action_4,
                                'action_5': database_form.action_5,
                                'action_6': database_form.action_6,
                                'waste_des_1': database_form.waste_des_1,
                                'waste_des_2': database_form.waste_des_2,
                                'waste_des_3': database_form.waste_des_3,
                                'waste_des_4': database_form.waste_des_4,
                                'containers_1': database_form.containers_1,
                                'containers_2': database_form.containers_2,
                                'containers_3': database_form.containers_3,
                                'containers_4': database_form.containers_4,
                                'waste_codes_1': database_form.waste_codes_1,
                                'waste_codes_2': database_form.waste_codes_2,
                                'waste_codes_3': database_form.waste_codes_3,
                                'waste_codes_4': database_form.waste_codes_4,
                                'dates_1': database_form.dates_1,
                                'dates_2': database_form.dates_2,
                                'dates_3': database_form.dates_3,
                                'dates_4': database_form.dates_4,
                            }
                            data = formF4_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF4_form(request.POST, instance=database_form)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-4')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'date': todays_log.date_save,
                                'observer': full_name
                            }
                            data = formF4_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF4_form(request.POST)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-4')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name
                }
                data = formF4_form(initial=initial_data)
                if request.method == "POST":
                    form = formF4_form(request.POST)
                    if form.is_valid():
                        form.save()

                        done = Forms.objects.filter(form='F-4')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formF4.html", {
        "back": back, 'todays_log': todays_log, 'data': data, "today": today, 'selector': selector, 'profile': profile, 'formName': formName
    })


@lock
def formF5(request, selector):
    formName = "F5"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    form_all = formF5_model.objects.count()

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if form_all == 0:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name
            }
            data = formF5_form(initial=initial_data)
            if request.method == "POST":
                form = formF5_form(request.POST)
                if form.is_valid():

                    form.save()

                    done = Forms.objects.filter(form='F-5')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')

        else:
            if today.weekday() not in {0, 1, 5, 6}:
                org = formF5_model.objects.all().order_by('-date')
                database_form = org[0]
                if today.weekday() == 2:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'observer': database_form.observer,
                            'time': database_form.time,
                            'date': database_form.date,
                            'retain_date': database_form.retain_date,
                            'status_1': database_form.status_1,
                            'status_2': database_form.status_2,
                            'status_3': database_form.status_3,
                            'status_4': database_form.status_4,
                            'status_5': database_form.status_5,
                            'status_6': database_form.status_6,
                            'status_7': database_form.status_7,
                            'comments_1': database_form.comments_1,
                            'comments_2': database_form.comments_2,
                            'comments_3': database_form.comments_3,
                            'comments_4': database_form.comments_4,
                            'comments_5': database_form.comments_5,
                            'comments_6': database_form.comments_6,
                            'comments_7': database_form.comments_7,
                            'action_1': database_form.action_1,
                            'action_2': database_form.action_2,
                            'action_3': database_form.action_3,
                            'action_4': database_form.action_4,
                            'action_5': database_form.action_5,
                            'action_6': database_form.action_6,
                            'action_7': database_form.action_7,
                            'waste_des_1': database_form.waste_des_1,
                            'waste_des_2': database_form.waste_des_2,
                            'waste_des_3': database_form.waste_des_3,
                            'waste_des_4': database_form.waste_des_4,
                            'containers_1': database_form.containers_1,
                            'containers_2': database_form.containers_2,
                            'containers_3': database_form.containers_3,
                            'containers_4': database_form.containers_4,
                            'waste_codes_1': database_form.waste_codes_1,
                            'waste_codes_2': database_form.waste_codes_2,
                            'waste_codes_3': database_form.waste_codes_3,
                            'waste_codes_4': database_form.waste_codes_4,
                            'dates_1': database_form.dates_1,
                            'dates_2': database_form.dates_2,
                            'dates_3': database_form.dates_3,
                            'dates_4': database_form.dates_4,
                        }
                        data = formF5_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF5_form(request.POST, instance=database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-5')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name
                        }
                        data = formF5_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF5_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-5')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    if today.weekday() in {3, 4}:
                        last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                        if last_wed == database_form.date:
                            initial_data = {
                                'observer': database_form.observer,
                                'time': database_form.time,
                                'date': database_form.date,
                                'retain_date': database_form.retain_date,
                                'status_1': database_form.status_1,
                                'status_2': database_form.status_2,
                                'status_3': database_form.status_3,
                                'status_4': database_form.status_4,
                                'status_5': database_form.status_5,
                                'status_6': database_form.status_6,
                                'comments_1': database_form.comments_1,
                                'comments_2': database_form.comments_2,
                                'comments_3': database_form.comments_3,
                                'comments_4': database_form.comments_4,
                                'comments_5': database_form.comments_5,
                                'comments_6': database_form.comments_6,
                                'action_1': database_form.action_1,
                                'action_2': database_form.action_2,
                                'action_3': database_form.action_3,
                                'action_4': database_form.action_4,
                                'action_5': database_form.action_5,
                                'action_6': database_form.action_6,
                                'waste_des_1': database_form.waste_des_1,
                                'waste_des_2': database_form.waste_des_2,
                                'waste_des_3': database_form.waste_des_3,
                                'waste_des_4': database_form.waste_des_4,
                                'containers_1': database_form.containers_1,
                                'containers_2': database_form.containers_2,
                                'containers_3': database_form.containers_3,
                                'containers_4': database_form.containers_4,
                                'waste_codes_1': database_form.waste_codes_1,
                                'waste_codes_2': database_form.waste_codes_2,
                                'waste_codes_3': database_form.waste_codes_3,
                                'waste_codes_4': database_form.waste_codes_4,
                                'dates_1': database_form.dates_1,
                                'dates_2': database_form.dates_2,
                                'dates_3': database_form.dates_3,
                                'dates_4': database_form.dates_4,
                            }
                            data = formF5_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF5_form(request.POST, instance=database_form)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-5')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'date': todays_log.date_save,
                                'observer': full_name
                            }
                            data = formF5_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF5_form(request.POST)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-5')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name
                }
                data = formF5_form(initial=initial_data)
                if request.method == "POST":
                    form = formF5_form(request.POST)
                    if form.is_valid():
                        form.save()

                        done = Forms.objects.filter(form='F-5')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formF5.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector': selector, 'profile': profile, 'formName': formName
    })


@lock
def formF6(request, selector):
    formName = "F6"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    form_all = formF6_model.objects.count()

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if form_all == 0:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name
            }
            data = formF6_form(initial=initial_data)
            if request.method == "POST":
                form = formF6_form(request.POST)
                if form.is_valid():

                    form.save()

                    done = Forms.objects.filter(form='F-6')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')

        else:
            if today.weekday() not in {0, 1, 5, 6}:
                org = formF6_model.objects.all().order_by('-date')
                database_form = org[0]
                if today.weekday() == 2:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'observer': database_form.observer,
                            'time': database_form.time,
                            'date': database_form.date,
                            'retain_date': database_form.retain_date,
                            'status_1': database_form.status_1,
                            'status_2': database_form.status_2,
                            'status_3': database_form.status_3,
                            'status_4': database_form.status_4,
                            'status_5': database_form.status_5,
                            'status_6': database_form.status_6,
                            'status_7': database_form.status_7,
                            'comments_1': database_form.comments_1,
                            'comments_2': database_form.comments_2,
                            'comments_3': database_form.comments_3,
                            'comments_4': database_form.comments_4,
                            'comments_5': database_form.comments_5,
                            'comments_6': database_form.comments_6,
                            'comments_7': database_form.comments_7,
                            'action_1': database_form.action_1,
                            'action_2': database_form.action_2,
                            'action_3': database_form.action_3,
                            'action_4': database_form.action_4,
                            'action_5': database_form.action_5,
                            'action_6': database_form.action_6,
                            'action_7': database_form.action_7,
                            'waste_des_1': database_form.waste_des_1,
                            'waste_des_2': database_form.waste_des_2,
                            'waste_des_3': database_form.waste_des_3,
                            'waste_des_4': database_form.waste_des_4,
                            'containers_1': database_form.containers_1,
                            'containers_2': database_form.containers_2,
                            'containers_3': database_form.containers_3,
                            'containers_4': database_form.containers_4,
                            'waste_codes_1': database_form.waste_codes_1,
                            'waste_codes_2': database_form.waste_codes_2,
                            'waste_codes_3': database_form.waste_codes_3,
                            'waste_codes_4': database_form.waste_codes_4,
                            'dates_1': database_form.dates_1,
                            'dates_2': database_form.dates_2,
                            'dates_3': database_form.dates_3,
                            'dates_4': database_form.dates_4,
                        }
                        data = formF6_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF6_form(request.POST, instance=database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-6')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name
                        }
                        data = formF6_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF6_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-6')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    if today.weekday() in {3, 4}:
                        last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                        if last_wed == database_form.date:
                            initial_data = {
                                'observer': database_form.observer,
                                'time': database_form.time,
                                'date': database_form.date,
                                'retain_date': database_form.retain_date,
                                'status_1': database_form.status_1,
                                'status_2': database_form.status_2,
                                'status_3': database_form.status_3,
                                'status_4': database_form.status_4,
                                'status_5': database_form.status_5,
                                'status_6': database_form.status_6,
                                'comments_1': database_form.comments_1,
                                'comments_2': database_form.comments_2,
                                'comments_3': database_form.comments_3,
                                'comments_4': database_form.comments_4,
                                'comments_5': database_form.comments_5,
                                'comments_6': database_form.comments_6,
                                'action_1': database_form.action_1,
                                'action_2': database_form.action_2,
                                'action_3': database_form.action_3,
                                'action_4': database_form.action_4,
                                'action_5': database_form.action_5,
                                'action_6': database_form.action_6,
                                'waste_des_1': database_form.waste_des_1,
                                'waste_des_2': database_form.waste_des_2,
                                'waste_des_3': database_form.waste_des_3,
                                'waste_des_4': database_form.waste_des_4,
                                'containers_1': database_form.containers_1,
                                'containers_2': database_form.containers_2,
                                'containers_3': database_form.containers_3,
                                'containers_4': database_form.containers_4,
                                'waste_codes_1': database_form.waste_codes_1,
                                'waste_codes_2': database_form.waste_codes_2,
                                'waste_codes_3': database_form.waste_codes_3,
                                'waste_codes_4': database_form.waste_codes_4,
                                'dates_1': database_form.dates_1,
                                'dates_2': database_form.dates_2,
                                'dates_3': database_form.dates_3,
                                'dates_4': database_form.dates_4,
                            }
                            data = formF6_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF6_form(request.POST, instance=database_form)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-6')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'date': todays_log.date_save,
                                'observer': full_name
                            }
                            data = formF6_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF6_form(request.POST)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-6')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name
                }
                data = formF6_form(initial=initial_data)
                if request.method == "POST":
                    form = formF6_form(request.POST)
                    if form.is_valid():
                        form.save()

                        done = Forms.objects.filter(form='F-6')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formF6.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector': selector, 'profile': profile, 'formName': formName
    })


@lock
def formF7(request, selector):
    formName = "F7"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    now = datetime.datetime.now()
    today = datetime.date.today()
    form_all = formF7_model.objects.count()

    full_name = request.user.get_full_name()

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if form_all == 0:
            initial_data = {
                'date': todays_log.date_save,
                'observer': full_name
            }
            data = formF7_form(initial=initial_data)
            if request.method == "POST":
                form = formF7_form(request.POST)
                if form.is_valid():

                    form.save()

                    done = Forms.objects.filter(form='F-7')[0]
                    done.submitted = True
                    done.date_submitted = todays_log.date_save
                    done.save()

                    return redirect('IncompleteForms')

        else:
            if today.weekday() not in {0, 1, 5, 6}:
                org = formF7_model.objects.all().order_by('-date')
                database_form = org[0]
                if today.weekday() == 2:
                    if todays_log.date_save == database_form.date:
                        initial_data = {
                            'observer': database_form.observer,
                            'time': database_form.time,
                            'date': database_form.date,
                            'retain_date': database_form.retain_date,
                            'status_1': database_form.status_1,
                            'status_2': database_form.status_2,
                            'status_3': database_form.status_3,
                            'status_4': database_form.status_4,
                            'status_5': database_form.status_5,
                            'status_6': database_form.status_6,
                            'status_7': database_form.status_7,
                            'comments_1': database_form.comments_1,
                            'comments_2': database_form.comments_2,
                            'comments_3': database_form.comments_3,
                            'comments_4': database_form.comments_4,
                            'comments_5': database_form.comments_5,
                            'comments_6': database_form.comments_6,
                            'comments_7': database_form.comments_7,
                            'action_1': database_form.action_1,
                            'action_2': database_form.action_2,
                            'action_3': database_form.action_3,
                            'action_4': database_form.action_4,
                            'action_5': database_form.action_5,
                            'action_6': database_form.action_6,
                            'action_7': database_form.action_7,
                            'waste_des_1': database_form.waste_des_1,
                            'waste_des_2': database_form.waste_des_2,
                            'waste_des_3': database_form.waste_des_3,
                            'waste_des_4': database_form.waste_des_4,
                            'containers_1': database_form.containers_1,
                            'containers_2': database_form.containers_2,
                            'containers_3': database_form.containers_3,
                            'containers_4': database_form.containers_4,
                            'waste_codes_1': database_form.waste_codes_1,
                            'waste_codes_2': database_form.waste_codes_2,
                            'waste_codes_3': database_form.waste_codes_3,
                            'waste_codes_4': database_form.waste_codes_4,
                            'dates_1': database_form.dates_1,
                            'dates_2': database_form.dates_2,
                            'dates_3': database_form.dates_3,
                            'dates_4': database_form.dates_4,
                        }
                        data = formF7_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF7_form(request.POST, instance=database_form)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-7')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'date': todays_log.date_save,
                            'observer': full_name
                        }
                        data = formF7_form(initial=initial_data)
                        if request.method == "POST":
                            form = formF7_form(request.POST)
                            if form.is_valid():
                                form.save()

                                done = Forms.objects.filter(form='F-7')[0]
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()

                                return redirect('IncompleteForms')
                else:
                    if today.weekday() in {3, 4}:
                        last_wed = todays_log.date_save - datetime.timedelta(days=today.weekday() - 2)
                        if last_wed == database_form.date:
                            initial_data = {
                                'observer': database_form.observer,
                                'time': database_form.time,
                                'date': database_form.date,
                                'retain_date': database_form.retain_date,
                                'status_1': database_form.status_1,
                                'status_2': database_form.status_2,
                                'status_3': database_form.status_3,
                                'status_4': database_form.status_4,
                                'status_5': database_form.status_5,
                                'status_6': database_form.status_6,
                                'comments_1': database_form.comments_1,
                                'comments_2': database_form.comments_2,
                                'comments_3': database_form.comments_3,
                                'comments_4': database_form.comments_4,
                                'comments_5': database_form.comments_5,
                                'comments_6': database_form.comments_6,
                                'action_1': database_form.action_1,
                                'action_2': database_form.action_2,
                                'action_3': database_form.action_3,
                                'action_4': database_form.action_4,
                                'action_5': database_form.action_5,
                                'action_6': database_form.action_6,
                                'waste_des_1': database_form.waste_des_1,
                                'waste_des_2': database_form.waste_des_2,
                                'waste_des_3': database_form.waste_des_3,
                                'waste_des_4': database_form.waste_des_4,
                                'containers_1': database_form.containers_1,
                                'containers_2': database_form.containers_2,
                                'containers_3': database_form.containers_3,
                                'containers_4': database_form.containers_4,
                                'waste_codes_1': database_form.waste_codes_1,
                                'waste_codes_2': database_form.waste_codes_2,
                                'waste_codes_3': database_form.waste_codes_3,
                                'waste_codes_4': database_form.waste_codes_4,
                                'dates_1': database_form.dates_1,
                                'dates_2': database_form.dates_2,
                                'dates_3': database_form.dates_3,
                                'dates_4': database_form.dates_4,
                            }
                            data = formF7_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF7_form(request.POST, instance=database_form)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-7')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
                        else:
                            initial_data = {
                                'date': todays_log.date_save,
                                'observer': full_name
                            }
                            data = formF7_form(initial=initial_data)
                            if request.method == "POST":
                                form = formF7_form(request.POST)
                                if form.is_valid():
                                    form.save()

                                    done = Forms.objects.filter(form='F-7')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()

                                    return redirect('IncompleteForms')
            else:
                initial_data = {
                    'date': todays_log.date_save,
                    'observer': full_name
                }
                data = formF7_form(initial=initial_data)
                if request.method == "POST":
                    form = formF7_form(request.POST)
                    if form.is_valid():
                        form.save()

                        done = Forms.objects.filter(form='F-7')[0]
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()

                        return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formF7.html", {
        "back": back, 'todays_log': todays_log, 'data': data, 'selector': selector, 'profile': profile, 'formName': formName
    })
