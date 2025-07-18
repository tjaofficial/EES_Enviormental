from django.shortcuts import render, redirect # type: ignore
from ..models import user_profile_model, Forms, Event, User, sop_model, facility_model, form22_model, form_settings_model
from ..forms import events_form, sop_form, user_profile_form, UserChangeForm
from datetime import datetime
import calendar
from django.core.exceptions import FieldError # type: ignore
from django.db.models import Q # type: ignore
from django.apps import apps # type: ignore
from ..utils.main_utils import setUnlockClientSupervisor, checkIfFacilitySelected, getCompanyFacilities, setUnlockClientSupervisor
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR, USE_S3
import os
from django.utils.text import slugify # type: ignore
from django.http import JsonResponse # type: ignore
import json
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.apps import apps # type: ignore

lock = login_required(login_url='Login')

@lock
def sidebar_data(request):
    facility = getattr(request, 'facility', None)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sidebar_data = {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility
    }
    return render(request, "supervisor/components/sup_sideBar.html", sidebar_data)

@lock
def search_forms_view(request, facility, access_page):
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    readingsData = False
    ModelForms = Forms.objects.all()
    weekend = False
    monthList =''
    options = facility_model.objects.all()
    profile = user_profile_model.objects.all()
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    formSettingsModel = form_settings_model.objects.filter(facilityChoice__facility_name=facility)
    if access_page != 'search':
        fsID = int(access_page.split("-")[1])
        access_page = access_page[:-4]
        if access_page != 'formN_model':
            chk_database = apps.get_model('EES_Forms', access_page).objects.count()
            print(apps.get_model('EES_Forms', access_page).objects.all())
            mainList = []
            # DATE - DAILY = 1, href="../Daily/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.date.year }}-{% if x.date.month < 10 %}0{{x.date.month}}{%else%}{{x.date.month}}{% endif %}-{% if x.date.day < 10 %}0{{x.date.day}}{%else%}{{x.date.day}}{% endif %}"
            # DATE - WEEKLY = 4, href="../Weekly/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.date.year }}-{% if x.date.month < 10 %}0{{x.date.month}}{%else%}{{x.date.month}}{% endif %}-{% if x.date.day < 10 %}0{{x.date.day}}{%else%}{{x.date.day}}{% endif %}{% if weekend %}/{% if x.weekend_day == 5 %}Saturday{% else %}Sunday{% endif %}{% else %}{% endif %}"
            # WEEK - DAILY = 3, href="../Daily/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.week_start.year }}-{% if x.week_start.month < 10 %}0{{x.week_start.month}}{%else%}{{x.week_start.month}}{% endif %}-{% if x.week_start.day < 10 %}0{{x.week_start.day}}{%else%}{{x.week_start.day}}{% endif %}"
            # WEEK - WEEKLY = 2, href="../Weekly/form{% if access_page.5 == '_' %}{{ access_page.4 }}{% else %}{{ access_page.4 }}{{ access_page.5}}{% endif %}/{{ x.week_start.year }}-{% if x.week_start.month < 10 %}0{{x.week_start.month}}{%else%}{{x.week_start.month}}{% endif %}-{% if x.week_start.day < 10 %}0{{x.week_start.day}}{%else%}{{x.week_start.day}}{% endif %}"
            if chk_database == 0:
                att_check = 5
                database = ''
            else:
                try:
                    # THESE ARE FORMS USING DATE
                    database = apps.get_model('EES_Forms', access_page).objects.all().filter(facilityChoice__facility_name=facility).order_by('-date')
                    print('BY DATE')
                    print(database.count())
                    if database.count() == 0:
                        att_check = 5
                        database = ''
                    else:
                        for x in ModelForms:
                            if x.form == access_page[4] or x.form == access_page[4] + '-' + access_page[5] or x.form == access_page[0:-6].replace('_', ' ').title() or x.link == access_page[:6]:
                                print("The follow model can be used to find forms:")
                                print(access_page)
                                if x.frequency[0] == 'W':
                                    # THESE ARE WEEKLY FORMS
                                    att_check = 4
                                    if x.weekend_only:
                                        weekend = True
                                    else:
                                        weekend = False
                                elif x.frequency[0] == 'M':
                                    att_check = 6
                                elif x.frequency[0] == 'Q':
                                    att_check = 7
                                else:
                                    # THESE ARE DAILY FORMS
                                    att_check = 1
                            else:
                                print('-')
                except FieldError as e:
                    # THESE ARE FORMS USING WEEK
                    database = apps.get_model('EES_Forms', access_page).objects.all().filter(facilityChoice__facility_name=facility).order_by('-week_start')
                    print('BY WEEK START')
                    print(database.count())
                    if database.count() == 0:
                        att_check = 5
                        database = ''
                    else:
                        for x in ModelForms:
                            print(x)
                            if x.form == access_page[4] or x.form == access_page[4] + '-' + access_page[5] or x.link == access_page[:6]:
                                # FORMS THAT ARE SINGLE DIDGITS
                                print('it does)')
                                if x.frequency[0] == 'D':
                                    # THESE ARE DAILY FORMS
                                    att_check = 3
                                else:
                                    # THESE ARE WEEKLY FORMS
                                    att_check = 2
                            else:
                                print('Error - EES_00006')
                print(att_check)
                if att_check == 1:
                    for x in database:
                        mainList.append([access_page, x.date, x, 'Daily'])
                        print(mainList)
                elif att_check == 2:
                    for x in database:
                        mainList.append([access_page, x.week_start, x, 'Weekly'])
                elif att_check == 3:
                    for x in database:
                        mainList.append([access_page, x.week_start, x, 'Daily'])
                elif att_check == 4:
                    if not weekend:
                        for x in database:
                            mainList.append([access_page, x.date, x, 'Weekly'])
                    else:
                        for x in database:
                            mainList.append([access_page, x.date, x, 'Weekly', '/' + x.weekend_day])
                elif att_check == 6:
                    for x in database:
                        mainList.append([access_page, x.date, x, 'Monthly'])
                elif att_check == 7:
                    for x in database:
                        mainList.append([access_page, x.date, x, 'Quarterly'])
                        
                        
                try:
                    Model2 = apps.get_model('EES_Forms', access_page[0:7] + 'readings_model')
                    readingsData = True
                    if len(Model2.objects.all()) > 0:
                        database2 = Model2.objects.all().filter(form__facilityChoice__facility_name=facility).order_by('-form')
                    else:
                        database2 = 'empty'
                except LookupError:
                    try:
                        Model2 = apps.get_model('EES_Forms', access_page[0:6] + 'readings_model')
                        readingsData = True
                        if len(Model2.objects.all()) > 0:
                            database2 = Model2.objects.all().filter(form__facilityChoice__facility_name=facility).order_by('-form')
                        else:
                            database2 = 'empty'
                    except LookupError:
                        readingsData = False
                        database2 = ''
        else:
            mainList=''
            database=''
            database2=''
            att_check=''
            queryN = form22_model.objects.all().filter(facilityChoice__facility_name=facility)
            monthList = []
            eliminator =[]
            for month in queryN:
                if month.date.month not in eliminator:
                    monthList.append((month.date.month, month.date.year, calendar.month_name[month.date.month],))
                    eliminator.append(month.date.month)
            print(monthList)
    else:
        mainList = ''
        fsID = ''
    if request.method == "POST":
        print('found it----------------')
        passedData = request.POST
        searchedText = passedData['searched'] if 'searched' in passedData.keys() else False
        database = ''
        database2 = ''
        att_check = ''
        mainList = ''
        weekend = False
        
        if searchedText:
            forms = formSettingsModel.filter(Q(formChoice__form__icontains=searchedText) | Q(formChoice__frequency__icontains=searchedText) | Q(formChoice__title__icontains=searchedText)).order_by('id')
            print(forms)
            letterForms = []
            for x in forms:
                modelName = f'form{x.formChoice.form}_model'
                letterForms.append([x, modelName, x.formChoice])
        else:
            messages.error(request,"Please enter a form 'Name' or 'Label' to search.")
            return redirect('archive', facility)
            
        return render(request, 'shared/search_forms.html', {
            'notifs': notifs, 
            'sortedFacilityData': sortedFacilityData, 
            'options': options, 
            'facility': facility, 
            'unlock': unlock, 
            'supervisor': supervisor, 
            'letterForms': letterForms, 
            'mainList': mainList, 
            'readingsData': readingsData, 
            'profile': profile, 
            'searched': searchedText, 
            'forms': forms, 
            'access_page': access_page, 
            'database': database, 
            'database2': database2, 
            'att_check': att_check, 
            'weekend': weekend, 
            'client': client,
        })
    else:
        return render(request, 'shared/search_forms.html', {
            'notifs': notifs, 
            'sortedFacilityData': sortedFacilityData, 
            'monthList': monthList, 
            'options': options, 
            'facility': facility, 
            'unlock': unlock, 
            'supervisor': supervisor, 
            'mainList': mainList, 
            'readingsData': readingsData, 
            'profile': profile, 
            'access_page': access_page, 
            'fsID': fsID,
            #'database': database, 
            #'database2': database2, 
            #'att_check': att_check, 
            'weekend': weekend, 
            'client': client,
        })

@lock
def profile_edit_view(request, userID):
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if client:
        return redirect('c_dashboard')
    elif unlock:
        return redirect('IncompleteForms')
    facilityList = getCompanyFacilities(request.user.user_profile.company.company_name)
    user_profiles = user_profile_model.objects.all()
    pic = ''
    
    if user_profiles.filter(user__id__exact=userID).exists():
        userProfileInfo = user_profiles.get(user__id__exact=userID)
        userInfo = User.objects.all().get(id__exact=userID)
        pic = userProfileInfo.profile_picture
        if userProfileInfo.phone:
            number = userProfileInfo.phone[2:]
            first = number[:3]
            middle = number[3:6]
            end = number[6:]
            parseNumber = '(' + first + ')' + middle + '-'+ end
        else:
            parseNumber = ''
        
    if request.method == 'POST':
        if request.POST.get('edit_user', False):
            print('CHECK 3')
            finalPhone = '+1' + ''.join(filter(str.isdigit, request.POST['phone']))
            new_data = request.POST.copy()
            new_data['phone'] = finalPhone
            new_data['company'] = userProfileInfo.company
            new_data['date_joined'] = userInfo.date_joined
            new_data['is_active'] = userInfo.is_active
            new_data['groups'] = userInfo.groups.all()[0]
            if 'id_facility_choice' in request.POST:
                new_data['facilityChoice'] = facility_model.objects.get(id=request.POST['id_facility_choice'])
            B = UserChangeForm(
                new_data,
                instance=userInfo
            )
            A = user_profile_form(
                new_data, 
                request.FILES, 
                instance=userProfileInfo
            )
            print(A.errors)
            print(B.errors)
            if A.is_valid() and B.is_valid():
                A.save()
                B.save()
                return redirect('Contacts')
    return render(request, "supervisor/profile_edits.html", {
        'notifs': notifs, 
        "unlock": unlock, 
        "client": client, 
        "supervisor": supervisor,
        'pic': pic, 
        'userInfo': userInfo,
        'userProfileInfo': userProfileInfo,
        'parseNumber': parseNumber,
        'facilityList': facilityList
    })

def handlePhone(number):
    number = number[2:]
    first = number[:3]
    middle = number[3:6]
    end = number[6:]
    parsedNumber = '(' + first +')'+ middle + '-' + end
    return parsedNumber
    
@lock
def shared_contacts_view(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    options = facility_model.objects.all()
    companyOfUser = user_profile_model.objects.get(user=request.user).company
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    
    companyProfiles = user_profile_model.objects.filter(company=companyOfUser).order_by('user')
    userProfile = companyProfiles.get(user__id=request.user.id)
    
    organized_list = []
    for index, user in enumerate(companyProfiles):
        if user.certs:
            certList = user.certs.split(',')
            i = 0
            for item in certList:
                certList[i] = certList[i].strip()
                i += 1
            organized_list.append((user.id, user, certList, handlePhone(user.phone)))
        else:
            organized_list.append((user.id, user, 'N/A' , handlePhone(user.phone)))
    
    if request.method == 'POST':
        answer = request.POST
        if 'facilitySelect' in request.POST.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard')
    return render(request, "shared/contacts.html", {
        'notifs': notifs, 
        'sortedFacilityData': sortedFacilityData, 
        'options': options, 
        'facility': facility, 
        'userProfile': userProfile, 
        'organized_list': organized_list, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock
    })
    
def format_sop_file_path(filename):
    # Replace spaces with underscores and fix the filename format
    base, ext = os.path.splitext(filename)
    formatted_filename = slugify(base).replace('-', '_') + ext
    return f'SOPs/{formatted_filename}'  # Set folder to "SOPs/"

@csrf_exempt
def delete_selected_sops(request, facility):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sop_ids = data.get('selected_sops', [])
            
            if sop_ids:
                sop_model.objects.filter(id__in=sop_ids).delete()
                return JsonResponse({'success': True, 'message': 'Selected SOPs deleted successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'No SOPs selected.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@lock
def sop_view(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    options = facility
    sops = sop_model.objects.filter(facilityChoice=facility).order_by('name')
    sopForm = sop_form()
    
    if request.method == 'POST':
        if 'facilitySelect' in request.POST.keys():
            if request.POST['facilitySelect'] != '':
                return redirect('sup_dashboard')
        # copyPost = request.POST.copy()
        # copyPost['facilityChoice'] = options
        # # print(request.FILES.url)
        # form = sop_form(copyPost, request.FILES)
        # print(form.errors)
        # if form.is_valid():
        #     A = form.save(commit=False)

        #     uploaded_file = request.FILES.get('pdf_file')
        #     if uploaded_file:
        #         formatted_path = format_sop_file_path(uploaded_file.name)
        #         A.pdf_file.name = f'{formatted_path}'  # Full S3 path under "media/SOPs/"

        #     A.pdf_url = A.pdf_file.url
        #     A.save()

        #     print("File Name:", A.pdf_file.name)  # Prints the file name
        #     print("File URL:", A.pdf_file.url)
        sop_id = request.POST.get('sop_id')
        name = request.POST.get('name')
        revision_date = request.POST.get('revision_date')
        pdf_file = request.FILES.get('pdf_file')

        if sop_id:  # Update existing SOP
            sop_instance = sop_model.objects.get(id=sop_id)
            sop_instance.name = name
            sop_instance.revision_date = revision_date
            if pdf_file:
                sop_instance.pdf_file = pdf_file  # Save the uploaded file
                sop_instance.save()
                sop_instance.pdf_url = sop_instance.pdf_file.url  # Now get the URL after saving
            sop_instance.save()
        else:  # Add new SOP
            new_sop = sop_model(
                name=name,
                revision_date=revision_date,
                pdf_file=pdf_file,
            )
            new_sop.facilityChoice = options
            new_sop.save()
            new_sop.pdf_url = new_sop.pdf_file.url  # Access URL after saving
            new_sop.save()

        return redirect('Sop', facility=facility)

    return render(request, 'shared/sops.html', {
        'sortedFacilityData':sortedFacilityData, 
        'notifs': notifs, 
        'options': options, 
        'facility': facility, 
        'sops': sops, 
        'sopForm': sopForm, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'AWS': USE_S3
    })
   
@lock 
def formsProgress(request, section):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    if unlock:
        return redirect('IncompleteForms')
    formSettingsModel = form_settings_model.objects.filter(facilityChoice=facility)
    finalList = {'Daily':[], 'Weekly':[], 'Monthly':[], 'Quarterly':[], 'Annually':[]}
    freqList = ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Annually']
    for x in formSettingsModel:
        formTitle = x.formChoice.header + ' - ' + x.formChoice.title
        if x.formChoice.frequency == 'Daily':
            finalList['Daily'].append((x.subChoice, formTitle, x.subChoice.submitted))
        elif x.formChoice.frequency == 'Weekly':
            finalList['Weekly'].append((x.subChoice, formTitle, x.subChoice.submitted))
        elif x.formChoice.frequency == 'Monthly':
            finalList['Monthly'].append((x.subChoice, formTitle, x.subChoice.submitted))
        elif x.formChoice.frequency == 'Quarterly':
            finalList['Quarterly'].append((x.subChoice, formTitle, x.subChoice.submitted))
        elif x.formChoice.frequency == 'Anually':
            finalList['Annually'].append((x.subChoice, formTitle, x.subChoice.submitted))
    for each in finalList:
        if len(finalList[each]) == 0:
            finalList[each] = 'No forms added'
        else:
            def myFunc(e):
                return e[0]
            finalList[each].sort(key=myFunc)          
    print(finalList)
    if request.method == 'POST':
        answer = request.POST
        if answer['facilitySelect'] != '':
            return redirect('sup_dashboard')
    return render(request, 'supervisor/formsProgress.html', {
        'notifs': notifs, 
        'finalList': finalList, 
        'facility': facility, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'sortedFacilityData': sortedFacilityData,
        'freqList': freqList
    })

@lock
def data_records(request):
    facility = getattr(request, 'facility', None)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)

    return render(request, "shared/data/data_records.html", {
        'facility': facility, 
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
    })