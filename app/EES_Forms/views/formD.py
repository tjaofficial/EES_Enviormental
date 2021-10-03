from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formD_model
from ..forms import formD_form
from ..utils import DBEmpty

lock = login_required(login_url='Login')
now = datetime.datetime.now()
back = Forms.objects.filter(form__exact='Incomplete Forms')


def new_form(request, week_almost, todays_log):
    if request.method == "POST":
        form = formD_form(request.POST)
        A_valid = form.is_valid()
        if A_valid:
            form.save()

            filled_out = True
            done = Forms.objects.filter(form='D')[0]
            for items in week_almost.whatever().values():
                if items is None:
                    filled_out = True
                    break

            if filled_out:
                done.submitted = True
                done.date_submitted = todays_log.date_save
                done.save()
            else:
                done.submitted = False
                done.save()

        return redirect('IncompleteForms')


@lock
def formD(request, selector):
    formName = "D"
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    today = datetime.date.today()
    last_friday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_friday + one_week

    week_start_dates = formD_model.objects.all().order_by('-week_start')

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        if not DBEmpty(week_start_dates):
            week_almost = week_start_dates[0]
            # last submitted saturday
            week = week_almost.week_start
            # week_fri = week_almost.week_end

            sunday = today - datetime.timedelta(days=1)

            if today.weekday() not in {5, 6}:
                if week == last_friday:
                    data = week_almost
                    initial_data = {
                        'week_start': data.week_start,
                        'week_end': data.week_end,
                        'truck_id1': data.truck_id1,
                        'date1': data.date1,
                        'time1': data.time1,
                        'contents1': data.contents1,
                        'freeboard1': data.freeboard1,
                        'wetted1': data.wetted1,
                        'comments1': data.comments1,
                        'truck_id2': data.truck_id2,
                        'date2': data.date2,
                        'time2': data.time2,
                        'contents2': data.contents2,
                        'freeboard2': data.freeboard2,
                        'wetted2': data.wetted2,
                        'comments2': data.comments2,
                        'truck_id3': data.truck_id3,
                        'date3': data.date3,
                        'time3': data.time3,
                        'contents3': data.contents3,
                        'freeboard3': data.freeboard3,
                        'wetted3': data.wetted3,
                        'comments3': data.comments3,
                        'truck_id4': data.truck_id4,
                        'date4': data.date4,
                        'time4': data.time4,
                        'contents4': data.contents4,
                        'freeboard4': data.freeboard4,
                        'wetted4': data.wetted4,
                        'comments4': data.comments4,
                        'truck_id5': data.truck_id5,
                        'date5': data.date5,
                        'time5': data.time5,
                        'contents5': data.contents5,
                        'freeboard5': data.freeboard5,
                        'wetted5': data.wetted5,
                        'comments5': data.comments5,
                        'observer1': data.observer1,
                        'observer2': data.observer2,
                        'observer3': data.observer3,
                        'observer4': data.observer4,
                        'observer5': data.observer5
                    }
                    empty_form = formD_form(initial=initial_data)

                    if request.method == "POST":
                        form = formD_form(request.POST, instance=data)
                        A_valid = form.is_valid()
                        if A_valid:
                            form.save()

                            filled_out = True
                            done = Forms.objects.filter(form='D')[0]
                            for items in week_almost.whatever().values():
                                if items is None:
                                    filled_out = True  # -change this back to false
                                    break

                            if filled_out:
                                done.submitted = True
                                done.date_submitted = todays_log.date_save
                                done.save()
                            else:
                                done.submitted = False
                                done.save()

                        return redirect('IncompleteForms')
                else:
                    initial_data = {
                        'week_start': last_friday,
                        'week_end': end_week
                    }
                    empty_form = formD_form(initial=initial_data)

                    new_form(request, week_almost, todays_log)
            else:
                if today.weekday() == 5:
                    if week == today:
                        data = week_almost
                        initial_data = {
                            'week_start': data.week_start,
                            'week_end': data.week_end,
                            'truck_id1': data.truck_id1,
                            'date1': data.date1,
                            'time1': data.time1,
                            'contents1': data.contents1,
                            'freeboard1': data.freeboard1,
                            'wetted1': data.wetted1,
                            'comments1': data.comments1,
                            'truck_id2': data.truck_id2,
                            'date2': data.date2,
                            'time2': data.time2,
                            'contents2': data.contents2,
                            'freeboard2': data.freeboard2,
                            'wetted2': data.wetted2,
                            'comments2': data.comments2,
                            'truck_id3': data.truck_id3,
                            'date3': data.date3,
                            'time3': data.time3,
                            'contents3': data.contents3,
                            'freeboard3': data.freeboard3,
                            'wetted3': data.wetted3,
                            'comments3': data.comments3,
                            'truck_id4': data.truck_id4,
                            'date4': data.date4,
                            'time4': data.time4,
                            'contents4': data.contents4,
                            'freeboard4': data.freeboard4,
                            'wetted4': data.wetted4,
                            'comments4': data.comments4,
                            'truck_id5': data.truck_id5,
                            'date5': data.date5,
                            'time5': data.time5,
                            'contents5': data.contents5,
                            'freeboard5': data.freeboard5,
                            'wetted5': data.wetted5,
                            'comments5': data.comments5,
                            'observer1': data.observer1,
                            'observer2': data.observer2,
                            'observer3': data.observer3,
                            'observer4': data.observer4,
                            'observer5': data.observer5,

                        }
                        empty_form = formD_form(initial=initial_data)
                        done = Forms.objects.filter(form='D')[0]
                        if request.method == "POST":
                            form = formD_form(request.POST, instance=week_almost)
                            A_valid = form.is_valid()
                            if A_valid:
                                form.save()
                                print('hello')
                                print('')
                                filled_out = True
                                for items in week_almost.whatever().values():
                                    if items is None:
                                        filled_out = False
                                        break

                                if filled_out:
                                    done = Forms.objects.filter(form='D')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()
                                else:
                                    done.submitted = False
                                    done.save()

                            return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'week_start': last_friday,
                            'week_end': end_week
                        }
                        empty_form = formD_form(initial=initial_data)

                        new_form(request, week_almost, todays_log)
                else:
                    sunday = today - datetime.timedelta(days=1)

                    if week == sunday:
                        data = week_almost
                        initial_data = {
                            'week_start': data.week_start,
                            'week_end': data.week_end,
                            'truck_id1': data.truck_id1,
                            'date1': data.date1,
                            'time1': data.time1,
                            'contents1': data.contents1,
                            'freeboard1': data.freeboard1,
                            'wetted1': data.wetted1,
                            'comments1': data.comments1,
                            'truck_id2': data.truck_id2,
                            'date2': data.date2,
                            'time2': data.time2,
                            'contents2': data.contents2,
                            'freeboard2': data.freeboard2,
                            'wetted2': data.wetted2,
                            'comments2': data.comments2,
                            'truck_id3': data.truck_id3,
                            'date3': data.date3,
                            'time3': data.time3,
                            'contents3': data.contents3,
                            'freeboard3': data.freeboard3,
                            'wetted3': data.wetted3,
                            'comments3': data.comments3,
                            'truck_id4': data.truck_id4,
                            'date4': data.date4,
                            'time4': data.time4,
                            'contents4': data.contents4,
                            'freeboard4': data.freeboard4,
                            'wetted4': data.wetted4,
                            'comments4': data.comments4,
                            'truck_id5': data.truck_id5,
                            'date5': data.date5,
                            'time5': data.time5,
                            'contents5': data.contents5,
                            'freeboard5': data.freeboard5,
                            'wetted5': data.wetted5,
                            'comments5': data.comments5,
                            'observer1': data.observer1,
                            'observer2': data.observer2,
                            'observer3': data.observer3,
                            'observer4': data.observer4,
                            'observer5': data.observer5,

                        }
                        empty_form = formD_form(initial=initial_data)
                        done = Forms.objects.filter(form='D')[0]
                        if request.method == "POST":
                            form = formD_form(request.POST, instance=data)
                            A_valid = form.is_valid()
                            if A_valid:
                                form.save()

                                filled_out = True
                                for items in week_almost.whatever().values():
                                    if items is None:
                                        filled_out = True  # -change this back to false
                                        break

                                if filled_out:
                                    done = Forms.objects.filter(form='D')[0]
                                    done.submitted = True
                                    done.date_submitted = todays_log.date_save
                                    done.save()
                                else:
                                    done.submitted = False
                                    done.save()

                            return redirect('IncompleteForms')
                    else:
                        initial_data = {
                            'week_start': sunday,
                            'week_end': sunday + one_week,
                        }
                        empty_form = formD_form(initial=initial_data)

                        new_form(request, week_almost, todays_log)
        else:
            initial_data = {
                'week_start': last_friday,
                'week_end': end_week
            }
            empty_form = formD_form(initial=initial_data)

            if request.method == "POST":
                form = formD_form(request.POST)
                A_valid = form.is_valid()
                if A_valid:
                    form.save()

                    filled_out = True
                    done = Forms.objects.filter(form='D')[0]

                    if filled_out:
                        done.submitted = True
                        done.date_submitted = todays_log.date_save
                        done.save()
                    else:
                        done.submitted = False
                        done.save()

                return redirect('IncompleteForms')
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formD.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'profile': profile, 'selector': selector, 'formName': formName
    })
