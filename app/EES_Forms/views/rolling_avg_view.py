from django.shortcuts import render # type: ignore
from django.http import JsonResponse # type: ignore
from datetime import timedelta, date, datetime
from ..utils.main_utils import setUnlockClientSupervisor
from django.contrib.auth.decorators import login_required # type: ignore
import math
from EES_Forms.models import form1_model, form2_model, form3_model, form4_model, form5_model, daily_battery_profile_model

lock = login_required(login_url='Login')

@lock
def rolling_average_page(request):
    facility = getattr(request, 'facility', None)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)

    return render(request, "shared/data/rolling_average.html",{
        'facility': facility, 
        'client': client, 
        "supervisor": supervisor, 
        "unlock": unlock
    })

@lock
def rolling_average_api(request):
    facility = request.session.get('facility')
    print(f"This is the facility: {facility}")
    if request.GET.get("date") and request.GET.get("date") != 'None':
        selected_date = str(request.GET.get("date"))
    else:
        selected_date = str(datetime.now().date())
    selected_date = date.fromisoformat(selected_date)

    start_date = selected_date - timedelta(days=29)
    charges_entries = form1_model.objects.filter(date__range=(start_date, selected_date)).order_by("date")
    doors_entries = form2_model.objects.filter(date__range=(start_date, selected_date)).order_by("date")
    lids_offtake_entries = form3_model.objects.filter(date__range=(start_date, selected_date)).order_by("date")
    battery_profile_entries = daily_battery_profile_model.objects.filter(date_save__range=(start_date, selected_date)).order_by("date_save")

    daily_data_list = {}
    for charge in charges_entries:
        charge_dict = [
            float(charge.ovens_data['charge_1']['c1_sec']),
            float(charge.ovens_data['charge_2']['c2_sec']),
            float(charge.ovens_data['charge_3']['c3_sec']),
            float(charge.ovens_data['charge_4']['c4_sec']),
            float(charge.ovens_data['charge_5']['c5_sec'])
        ]
        if str(charge.date) in daily_data_list:
            daily_data_list[str(charge.date)]['charges'] = charge_dict
        else:
            daily_data_list[str(charge.date)] = {
                "charges": charge_dict
            }
        print(daily_data_list)

    for bat_prof in battery_profile_entries:
        if str(bat_prof.date_save) in daily_data_list:
            daily_data_list[str(bat_prof.date_save)]['inoperable_ovens'] = bat_prof.inop_ovens

    for door in doors_entries:
        door_dict = {
            "not_observed": door.doors_not_observed,
            "leaks": door.leaking_doors,
            "door_percent_leaking": door.percent_leaking
        }
        if str(door.date) in daily_data_list:
            daily_data_list[str(door.date)]['doors'] = door_dict
        else:
            daily_data_list[str(door.date)] = {
                "doors": door_dict
            }

    for lid in lids_offtake_entries:
        lid_dict = {
            "lids_not_observed": lid.l_not_observed,
            "offtakes_not_observed": lid.om_not_observed,
            "lid_leaks": lid.l_leaks,
            "offtake_leaks": lid.om_leaks,
            "lids_percent_leaking": lid.l_percent_leaking,
            "offtakes_percent_leaking": lid.om_percent_leaking
        }
        if str(lid.date) in daily_data_list:
            daily_data_list[str(lid.date)]['lids_offtakes'] = lid_dict
        else:
            daily_data_list[str(lid.date)] = {
                "lids_offtakes": lid_dict
            }

    # Compute 30-day averages
    ln_30day_charges_list = []
    doors_30day_list = []
    lids_30day_list = []
    offtakes_30day_list = []

    for data_date, data_content in daily_data_list.items():
        ln_charge_list = []
        for charge in data_content['charges']:
            ln_charge_list.append(math.log(charge))
        sum_ln_charges = sum(ln_charge_list)
        #ln_avg_charge = math.exp(sum_ln_charges/len(ln_charge_list))-1
        ln_30day_charges_list.append(sum_ln_charges)
        if 'doors' in data_content:
            doors_30day_list.append(float(data_content['doors']['door_percent_leaking']))
        if 'lids_offtakes' in data_content:
            lids_30day_list.append(float(data_content['lids_offtakes']['lids_percent_leaking']))
            offtakes_30day_list.append(float(data_content['lids_offtakes']['offtakes_percent_leaking']))
    print(doors_30day_list)

    month_ln_avg_charge = math.exp(sum(ln_30day_charges_list)/150)-1
    month_avg_doors = sum(doors_30day_list)/30 if doors_30day_list else 0
    month_avg_lids = sum(lids_30day_list)/30 if lids_30day_list else 0
    month_avg_offtakes = sum(offtakes_30day_list)/30 if offtakes_30day_list else 0

    rolling_avg = {
        "doors_avg": month_avg_doors,
        "lids_avg": month_avg_lids,
        "offtakes_avg": month_avg_offtakes,
        "charges_avg": month_ln_avg_charge
    }

    selected_day_str = selected_date.isoformat()
    selected_day = daily_data_list.get(selected_day_str)
    if not selected_day and daily_data_list:
        latest_date = max(daily_data_list.keys())
        selected_day = daily_data_list[latest_date]

    return JsonResponse({
        "rolling_avg": rolling_avg,
        "selected_day": selected_day,
        "history": daily_data_list,
    })
