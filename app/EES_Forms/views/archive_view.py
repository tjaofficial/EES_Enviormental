from django.shortcuts import render, redirect # type: ignore
from django.http import JsonResponse # type: ignore
from django.db.models import Q # type: ignore
from django.urls import reverse # type: ignore
from django.apps import apps # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..utils.main_utils import setUnlockClientSupervisor, colorModeSwitch, checkIfFacilitySelected, getCompanyFacilities, setUnlockClientSupervisor
from datetime import datetime
from ..models import form_settings_model, facility_model

lock = login_required(login_url='Login')

@lock
def archive(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    archiveForm_query = request.GET.get('archiveFormID')
    archiveFormLabel_query = request.GET.get('archiveFormLabel')
    archiveMonth_query = request.GET.get('archiveMonth')
    archiveDate_query = request.GET.get('archiveDate')
    formSettingsModel = form_settings_model.objects.filter(facilityChoice=facility, settings__active=True)
    print(formSettingsModel)
    def getFsSearchID(itemSearched, fsModel):
        if itemSearched != '' and itemSearched is not None and fsModel.exists():
            fsList = []
            idSearchData = False
            itemSearched = int(itemSearched)
            print('check 1')
            print(fsModel)
            for fs in fsModel:
                print(int(fs.formChoice.form))
                print(itemSearched)
                if int(fs.formChoice.form) == itemSearched:
                    idSearchData = fs
                    break
            if idSearchData:
                link = str(idSearchData.formChoice.link) + '_model'
                chk_database = apps.get_model('EES_Forms', link).objects.filter(formSettings__facilityChoice__facility_name=facility)
                for item in chk_database:
                    fsList.append(item)
            return fsList
        else:
            return "none"
    
    def getFsSearchLabel(itemSearched, fsModel):
        if itemSearched != '' and itemSearched is not None and fsModel.exists():
            fsList1 = []
            print('Starting to search labels...')
            for fs in fsModel:
                fsPackets = fs.settings['packets']
                if fsPackets:
                    for packetLabel in fsPackets:
                        if fsPackets[packetLabel].lower() == itemSearched.lower():
                            if fs not in fsList1:
                                fsList1.append(fs)
            print(fsList1)
            modelsList = []
            for fsSort in fsList1:
                for model in apps.get_models():
                    if model.__name__[:4] == "form" and model.__name__[-6:] == '_model':
                        modelName = model.__name__[4:-6]
                        if str(modelName) == str(fsSort.formChoice.form):
                            modelsList.append((model, fsSort))
            fsList = []
            for item in modelsList:
                chk_database = item[0].objects.filter(formSettings=item[1])
                for iForm in chk_database:
                    if iForm not in fsList:
                        fsList.append(iForm)
            return fsList  
        else:
            return "none"
                            
    def getFsSearchMonthYear(itemSearched, fsModel):
        if itemSearched != "" and itemSearched is not None and fsModel.exists():
            itemSearched = datetime.strptime(itemSearched, "%Y-%m").date()
            # formIDList = []
            # for fs in fsModel:
            #     formIDList.append((fs.formChoice.id, fs))
            # print(formIDList)
            modelsList = []
            for model in apps.get_models():
                for fs in fsModel:
                    if model.__name__[:4] == "form" and model.__name__[-6:] == '_model':
                        modelName = model.__name__[4:-6]
                        if str(modelName) == str(fs.formChoice.form):
                            modelsList.append((model, fs))
            fsList = []
            for item in modelsList:
                try:
                    chk_database = item[0].objects.filter(Q(date__month=itemSearched.month) & Q(date__year=itemSearched.year))
                except:
                    chk_database = item[0].objects.filter(Q(week_start__month=itemSearched.month) & Q(week_start__year=itemSearched.year))
                for iForm in chk_database:
                    if iForm not in fsList:
                        fsList.append(iForm)
            return fsList  
        else:
            return "none"
 
    def getFsSearchDate(itemSearched, fsModel):
        if itemSearched != "" and itemSearched is not None and fsModel.exists():
            itemSearched = datetime.strptime(itemSearched, "%Y-%m-%d").date()
            modelsList = []
            for model in apps.get_models():
                for fs in fsModel:
                    if model.__name__[:4] == "form" and model.__name__[-6:] == '_model':
                        modelName = model.__name__[4:-6]
                        if str(modelName) == str(fs.formChoice.form):
                            modelsList.append((model, fs))
            fsList = []
            for item in modelsList:
                try:
                    chk_database = item[0].objects.filter(date=itemSearched)
                except:
                    chk_database = item[0].objects.filter(week_start=itemSearched)
                for iForm in chk_database:
                    if iForm not in fsList:
                        fsList.append(iForm)
            return fsList  
        else:
            return "none"
      
    IDQueryList = getFsSearchID(archiveForm_query, formSettingsModel)
    labelQueryList = getFsSearchLabel(archiveFormLabel_query, formSettingsModel)
    monthYearQueryList = getFsSearchMonthYear(archiveMonth_query, formSettingsModel)
    dateQueryList = getFsSearchDate(archiveDate_query, formSettingsModel)
    print(IDQueryList)
    sortList = []
    finalList = []
    if monthYearQueryList != 'none':
        finalList = monthYearQueryList
    if IDQueryList != 'none':
        if len(finalList) == 0:
            finalList = IDQueryList
        else:
            for sort2 in IDQueryList:
                if sort2 in finalList:
                    sortList.append(sort2)
            finalList = sortList
            sortList = []
    if labelQueryList != 'none':
        if len(finalList) == 0:
            finalList = labelQueryList
        else:
            for sort3 in labelQueryList:
                if sort3 in finalList:
                    sortList.append(sort3)
            finalList = sortList
            sortList = []
    if dateQueryList != 'none':
        if len(finalList) == 0:
            finalList = dateQueryList
        else:
            for sort4 in dateQueryList:
                if sort4 in finalList:
                    sortList.append(sort4)
            finalList = sortList

    # Needs code for sorting the finalList. Take and create dict or list but create
    # defining factor to be the date and then sort them.
    
    if request.method == 'POST':
        answer = request.POST
        if supervisor:
            if answer['facilitySelect'] != '':
                return redirect('archive', answer['facilitySelect'])
        else:
            if 'colorMode' in answer.keys():
                colorModeSwitch(request)

    return render(request, 'shared/archive.html', {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'facility': facility,
        'client': client, 
        "supervisor": supervisor, 
        "unlock": unlock, 
        'finalList': finalList,
    })

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
