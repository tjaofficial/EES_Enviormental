from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model
from ..forms import formG1_form, formG2_form, user_profile_form

lock = login_required(login_url='Login')
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formG1(request, selector):
    formName = "G1"
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        initial_data = {
            'date': todays_log.date_save,
            'estab': "EES COKE BATTERY",
            'county': "Wayne",
            'estab_no': "P0408",
            'equip_loc': "Zug Island",
            'district': "Detroit",
            'city': "River Rouge",
            'observer': full_name,
            'cert_date': cert_date,
            'process_equip1': "-",
            'process_equip2': "-",
            'op_mode1': "normal",
            'op_mode2': "normal",
            'emission_point_start': "Above Stack",
            'emission_point_stop': "Same",
            'height_above_ground': "150",
            'height_rel_observer': "150",
            'water_drolet_present': "No",
            'water_droplet_plume': "N/A",
            'describe_background_start': "Skies",
            'describe_background_stop': "Same"
        }
        data = formG1_form(initial=initial_data)
        profile_form = user_profile_form()
        # readings_form = formA5_readings_form()

        if request.method == "POST":
            form = formG1_form(request.POST)

            A_valid = form.is_valid()

            if A_valid:
                # A = form.save()

                done = Forms.objects.filter(form='G-1')[0]
                done.submitted = True
                done.save()

                return redirect('IncompleteForms')
        else:
            form = formG1_form(initial=initial_data)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Weekly/formG1.html", {
        "back": back, 'data': data, 'profile_form': profile_form,  'selector': selector, 'profile': profile, 'todays_log': todays_log, 'formName': formName
    })


@lock
def formG2(request, selector):
    formName = "G2"
    now = datetime.datetime.now()
    profile = user_profile_model.objects.all()
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        initial_data = {
            'date': todays_log.date_save,
            'estab': "EES COKE BATTERY",
            'county': "Wayne",
            'estab_no': "P0408",
            'equip_loc': "Zug Island",
            'district': "Detroit",
            'city': "River Rouge",
            'observer': full_name,
            'cert_date': cert_date,
            'process_equip1': "-",
            'process_equip2': "-",
            'op_mode1': "normal",
            'op_mode2': "normal",
            'emission_point_start': "Above Stack",
            'emission_point_stop': "Same",
            'height_above_ground': "150",
            'height_rel_observer': "150",
            'water_drolet_present': "No",
            'water_droplet_plume': "N/A",
            'describe_background_start': "Skies",
            'describe_background_stop': "Same"
        }
        data = formG2_form
        profile_form = user_profile_form()
        # readings_form = formA5_readings_form()

        if request.method == "POST":
            form = formG2_form(request.POST)

            A_valid = form.is_valid()

            if A_valid:
                # A = form.save()

                done = Forms.objects.filter(form='G-1')[0]
                done.submitted = True
                done.save()

                return redirect('IncompleteForms')
        else:
            form = formG2_form(initial=initial_data)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)

    return render(request, "Monthly/formG2.html", {
        "back": back, 'data': data, 'profile_form': profile_form,  'selector': selector, 'profile': profile, 'todays_log': todays_log, 'formName': formName
    })
