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
    week_start_dates = formD_model.objects.all().order_by('-week_start')

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]
        if len(week_start_dates) > 0:
            week_almost = week_start_dates[0]
            last_form_sat = week_almost.week_start
            if today.weekday() not in {5, 6}:
                if last_form_sat == last_saturday:
                    existing = True
            elif today.weekday() == 5:
                if last_form_sat == today:
                    existing = True
            elif last_form_sat == sunday:
                existing = True
        if existing:
            initial_data = {
                'week_start': week_almost.week_start,
                'week_end': week_almost.week_end,
                'truck_id1': week_almost.truck_id1,
                'date1': week_almost.date1,
                'time1': week_almost.time1,
                'contents1': week_almost.contents1,
                'freeboard1': week_almost.freeboard1,
                'wetted1': week_almost.wetted1,
                'comments1': week_almost.comments1,
                'truck_id2': week_almost.truck_id2,
                'date2': week_almost.date2,
                'time2': week_almost.time2,
                'contents2': week_almost.contents2,
                'freeboard2': week_almost.freeboard2,
                'wetted2': week_almost.wetted2,
                'comments2': week_almost.comments2,
                'truck_id3': week_almost.truck_id3,
                'date3': week_almost.date3,
                'time3': week_almost.time3,
                'contents3': week_almost.contents3,
                'freeboard3': week_almost.freeboard3,
                'wetted3': week_almost.wetted3,
                'comments3': week_almost.comments3,
                'truck_id4': week_almost.truck_id4,
                'date4': week_almost.date4,
                'time4': week_almost.time4,
                'contents4': week_almost.contents4,
                'freeboard4': week_almost.freeboard4,
                'wetted4': week_almost.wetted4,
                'comments4': week_almost.comments4,
                'truck_id5': week_almost.truck_id5,
                'date5': week_almost.date5,
                'time5': week_almost.time5,
                'contents5': week_almost.contents5,
                'freeboard5': week_almost.freeboard5,
                'wetted5': week_almost.wetted5,
                'comments5': week_almost.comments5,
                'observer1': week_almost.observer1,
                'observer2': week_almost.observer2,
                'observer3': week_almost.observer3,
                'observer4': week_almost.observer4,
                'observer5': week_almost.observer5
            }
        else:
            initial_data = {
                'week_start': last_saturday,
                'week_end': end_week
            }

        empty_form = formD_form(initial=initial_data)
        if request.method == "POST":
            if existing:
                form = formD_form(request.POST, instance=week_almost)
            else:
                form = formD_form(request.POST)
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
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formD.html", {
        "back": back, 'todays_log': todays_log, 'empty': empty_form, 'profile': profile, 'selector': selector, 'formName': formName
    })
