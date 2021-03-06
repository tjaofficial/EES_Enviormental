from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formD_model
from ..forms import formD_form

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formD(request, selector):
    formName = "D"
    existing = False
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')
    today = datetime.date.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    one_week = datetime.timedelta(days=6)
    end_week = last_saturday + one_week
    sunday = today - datetime.timedelta(days=1)
    submitted_forms = formD_model.objects.all().order_by('-week_start')

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if len(submitted_forms) > 0:
            latest_form = submitted_forms[0]
            starting_saturday = latest_form.week_start
            if today.weekday() not in {5, 6}:
                if starting_saturday == last_saturday:
                    existing = True
            elif today.weekday() == 5:
                if starting_saturday == today:
                    existing = True
            elif starting_saturday == sunday:
                existing = True
        print(existing)
        if existing:
            initial_data = {
                'week_start': latest_form.week_start,
                'week_end': latest_form.week_end,
                'truck_id1': latest_form.truck_id1,
                'date1': latest_form.date1,
                'time1': latest_form.time1,
                'contents1': latest_form.contents1,
                'freeboard1': latest_form.freeboard1,
                'wetted1': latest_form.wetted1,
                'comments1': latest_form.comments1,
                'truck_id2': latest_form.truck_id2,
                'date2': latest_form.date2,
                'time2': latest_form.time2,
                'contents2': latest_form.contents2,
                'freeboard2': latest_form.freeboard2,
                'wetted2': latest_form.wetted2,
                'comments2': latest_form.comments2,
                'truck_id3': latest_form.truck_id3,
                'date3': latest_form.date3,
                'time3': latest_form.time3,
                'contents3': latest_form.contents3,
                'freeboard3': latest_form.freeboard3,
                'wetted3': latest_form.wetted3,
                'comments3': latest_form.comments3,
                'truck_id4': latest_form.truck_id4,
                'date4': latest_form.date4,
                'time4': latest_form.time4,
                'contents4': latest_form.contents4,
                'freeboard4': latest_form.freeboard4,
                'wetted4': latest_form.wetted4,
                'comments4': latest_form.comments4,
                'truck_id5': latest_form.truck_id5,
                'date5': latest_form.date5,
                'time5': latest_form.time5,
                'contents5': latest_form.contents5,
                'freeboard5': latest_form.freeboard5,
                'wetted5': latest_form.wetted5,
                'comments5': latest_form.comments5,
                'observer1': latest_form.observer1,
                'observer2': latest_form.observer2,
                'observer3': latest_form.observer3,
                'observer4': latest_form.observer4,
                'observer5': latest_form.observer5
            }
        elif today.weekday() == 5:
            initial_data = {
                'week_start': today,
                'week_end': today + datetime.timedelta(days=6)
            }
        elif today.weekday() == 6:
            initial_data = {
                'week_start': today - datetime.timedelta(days=1),
                'week_end': today + datetime.timedelta(days=5)
            }
        else:
            initial_data = {
                'week_start': last_saturday,
                'week_end': end_week
            }

        empty_form = formD_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formD_form(request.POST, instance=latest_form)
            else:
                form = formD_form(request.POST)
            A_valid = form.is_valid()
            if A_valid:
                form.save()

                filled_out = True
                done = Forms.objects.filter(form='D')[0]
                for items in latest_form.whatever().values():
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
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formD.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'profile': profile, 'selector': selector, 'formName': formName
    })
