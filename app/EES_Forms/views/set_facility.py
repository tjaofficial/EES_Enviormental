from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.http import JsonResponse # type: ignore
import json

@csrf_exempt
def set_facility(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['selected_facility'] = data.get('id')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
