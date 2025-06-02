from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.http import JsonResponse # type: ignore
import json
from EES_Enviormental.settings import OBSER_VAR
from ..models import daily_battery_profile_model
from ..decor import group_required

@csrf_exempt
def set_facility(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['selected_facility'] = data.get('id')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@group_required(OBSER_VAR)
def check_bat_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        facility_id = data.get("facility_id")
        date = data.get("date")

        exists = daily_battery_profile_model.objects.filter(
            facilityChoice__id=facility_id,
            date_save=date
        ).exists()

        return JsonResponse({"exists": exists})
