from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from ..models import Forms, user_profile_model, daily_battery_profile_model, formH_model
from ..forms import formH_form, user_profile_form

lock = login_required(login_url='Login')
now = datetime.datetime.now()
back = Forms.objects.filter(form__exact='Incomplete Forms')


@lock
def formH(request, access_page):
    formName = "H"
    profile = user_profile_model.objects.all()
    full_name = request.user.get_full_name()
    cert_date = request.user.user_profile_model.cert_date
    daily_prof = daily_battery_profile_model.objects.all().order_by('-date_save')

    count_bp = daily_battery_profile_model.objects.count()

    if count_bp != 0:
        todays_log = daily_prof[0]

        org = formH_model.objects.all().order_by('-date')

        if access_page != 'form':
            for x in org:
                if str(x.date) == str(access_page):
                    database_model = x
            data = database_model
            profile_form = ''
        else:
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
                'height_above_ground': "300",
                'height_rel_observer': "300",
                'water_drolet_present': "No",
                'water_droplet_plume': "N/A",
                'describe_background_start': "Skies",
                'describe_background_stop': "Same"
            }
            data = formH_form(initial=initial_data)
            profile_form = user_profile_form()
            # readings_form = formA5_readings_form()

            if request.method == "POST":
                form = formH_form(request.POST)

                A_valid = form.is_valid()

                if A_valid:
                    # A = form.save()

                    done = Forms.objects.filter(form='H')[0]
                    done.submitted = True
                    done.save()

                    return redirect('IncompleteForms')
            else:
                form = formH_form(initial=initial_data)
    else:
        batt_prof = 'daily_battery_profile/login/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        return redirect(batt_prof)
    return render(request, "Weekly/formH.html", {
        "back": back, 'data': data, 'profile_form': profile_form, 'access_page': access_page, 'profile': profile, 'todays_log': todays_log, 'formName': formName
    })
