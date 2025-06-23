from django.http import JsonResponse # type: ignore
from django.db.models import Q # type: ignore
from django.urls import reverse # type: ignore
from django.apps import apps # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from datetime import datetime
from ..models import form_settings_model, facility_model

lock = login_required(login_url='Login')

@lock
def archive_search_api(request):
    facility = request.GET.get('facility', None)
    facility = facility_model.objects.get(facility_name=facility)
    if not facility or facility in ['None', 'null']:
        return JsonResponse({'error': 'Please select a facility first.'}, status=400)
    form_id = request.GET.get('formID', '')
    print(form_id)
    form_label = request.GET.get('formLabel', '')
    form_month = request.GET.get('formMonth', '')
    form_date = request.GET.get('formDate', '')
    form_settings_qs = form_settings_model.objects.filter(facilityChoice=facility, settings__active=True)
    print(form_settings_qs)
    if form_id:
        print("query id")
        form_settings_qs = form_settings_qs.filter(formChoice__form=form_id)
        print(form_settings_qs)

    if form_label:
        print("query label")
        form_settings_qs = form_settings_qs.filter(
            Q(settings__packets__icontains=form_label)
        )
    
    if not form_settings_qs.exists():
        return JsonResponse({'results': []})

    final_results = []

    for fs in form_settings_qs:
        model_name = f"form{fs.formChoice.form}_model"
        try:
            form_model = apps.get_model('EES_Forms', model_name)
        except LookupError:
            continue  # skip if model doesn't exist

        form_query = Q()

        # Handle date fields (some forms have date, others have week_start)
        date_field = 'date'
        if hasattr(form_model, 'week_start'):
            date_field = 'week_start'

        if form_month:
            year, month = form_month.split('-')
            kwargs = {
                f"{date_field}__year": int(year),
                f"{date_field}__month": int(month)
            }
            form_query &= Q(**kwargs)

        if form_date:
            try:
                date_obj = datetime.strptime(form_date, "%Y-%m-%d").date()
                kwargs = {f"{date_field}": date_obj}
                form_query &= Q(**kwargs)
            except:
                pass  # invalid date format gracefully ignored

        form_records = form_model.objects.filter(formSettings=fs).filter(form_query)

        for record in form_records:
            # Build your URL logic exactly like you had before:
            if str(fs.formChoice.form) in ['20', '6', '21', '8']:
                form_url = reverse(fs.formChoice.link, args=[fs.id, record.week_start])
            else:
                form_url = reverse(fs.formChoice.link, args=[fs.id, record.date])

            # Format packets nicely
            packets = fs.settings.get('packets', {})
            packet_labels = list(packets.values())

            final_results.append({
                'form_id': fs.id,
                'form_labels': packet_labels,
                'form_title': fs.settings['settings'].get('custom_name') or fs.formChoice.title,
                'form_header': fs.formChoice.header,
                'date': str(getattr(record, date_field)),
                'url': form_url,
            })
    print(f"Your looking for this {final_results}")
    return JsonResponse({'results': final_results})
