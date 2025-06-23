from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Q # type: ignore
from ..utils.main_utils import parsePhone, setDefaultSettings, dashDictOptions, checkIfFacilitySelected, setUnlockClientSupervisor, braintreeGateway, getCompanyFacilities, defaultNotifications
from ..models import user_profile_model, company_model, User, braintree_model, braintreePlans, facility_model, account_reactivation_model
from ..forms import CreateUserForm, user_profile_form, company_Update_form, bat_info_form
from EES_Enviormental.settings import SUPER_VAR
from datetime import datetime
import json
from ..decor import group_required


lock = login_required(login_url='Login')

@lock
def sup_account_view(request):
    facility = getattr(request, 'facility', None)
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    stripeData = request.user.user_profile.company.subscription # need to fix this

    sortedFacilityData = getCompanyFacilities(request.user.user_profile.company.company_name)
    userProfileQuery = user_profile_model.objects.all()
    accountData = request.user.user_profile
    userCompany = accountData.company
    listOfEmployees = userProfileQuery.filter(~Q(position="client"), company=userCompany)
    companyStatus = stripeData.status
    current_date = datetime.today().date()
    end_of_billing_date = datetime.strptime(stripeData.settings['next_billing_date'], "%Y-%m-%d").date() if stripeData.settings['next_billing_date'] and stripeData.settings['next_billing_date'] not in ['None', 'none'] else False
    if companyStatus == 'active' or companyStatus == 'canceled' and end_of_billing_date and current_date <= end_of_billing_date:
        active_registrations = len(listOfEmployees.filter(user__is_active=True))
    else:
        active_registrations = 0
    print(str(current_date))
    reactivationQuery = account_reactivation_model.objects.all()
        
    if request.method == "POST":
        data = request.POST
        if 'facilitySelect' in data.keys():
            if data['facilitySelect'] != '':
                return redirect('sup_dashboard', data['facilitySelect'])
        elif 'cancelReg' in data.keys():
            print(data)
            selectedRegister = userProfileQuery.get(id=int(data['registerID'])).user
            selectedRegister.is_active = False
            selectedRegister.save()
            reactivation = account_reactivation_model.objects.filter(user=selectedRegister)
            if reactivation.exists():
                reactivation[0].delete()

            return redirect("Account", facility)
        elif 'activateReg' in data.keys():
            print(data)
            userProf = userProfileQuery.get(id=int(data['registerID']))
            leadSup = userProfileQuery.get(company=userProf.company, settings__position="supervisor-m")
            braintree = braintree_model.objects.get(user=leadSup.user)

            new_entry = account_reactivation_model(
                user = userProf.user,
                reactivation_date = braintree.settings['subscription']['next_billing_date']
            )
            new_entry.save()

            return redirect("Account", facility)
    return render(request, 'supervisor/settings/sup_account.html',{
        'notifs': notifs,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'sortedFacilityData': sortedFacilityData,
        'facility': facility,
        'accountData': accountData,
        'listOfEmployees': listOfEmployees,
        'stripeData': stripeData,
        'active_registrations': active_registrations,
        'userProfileQuery': userProfileQuery,
        'today': (current_date, end_of_billing_date),
        'reactivationQuery': reactivationQuery
    })

@lock
def sup_update_account(request, selector):
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    user = request.user
    variables = {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'notifs': notifs,
        'selector': selector
    }
    if selector == "account":
        primaryModel = ""
        initial_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'cert_date': user.user_profile.cert_date,
            'phone': parsePhone(user.user_profile.phone),
            'certs': user.user_profile.certs,
            'profile_picture': user.user_profile.profile_picture,
        }
    elif selector == "company":
        primaryModel = company_model.objects.get(id=user.user_profile.company.id)
        initial_data = {
            'company_name': primaryModel.company_name,
            'address': primaryModel.address,
            'city': primaryModel.city,
            'state': primaryModel.state,
            'zipcode': primaryModel.zipcode,
            'phone': parsePhone(primaryModel.phone),
            'icon': primaryModel.icon
        }
        primaryForm = company_Update_form(initial=initial_data)
        variables['primaryForm'] = primaryForm

    variables['initial_data'] = initial_data
    if request.method == 'POST':
        print(request.POST)
        dataFromForm = request.POST
        if selector == "account":
            primaryModel.first_name = dataFromForm['first_name']
            primaryModel.last_name = dataFromForm['last_name']
            primaryModel.username = dataFromForm['username']
            primaryModel.email = dataFromForm['email']
            if unlock:
                user.cert_date = dataFromForm['cert_date']
            user.phone = parsePhone(dataFromForm['phone'])
            if dataFromForm['two_factor_enabled'] == "no":
                user.settings['profile']['two_factor_enabled'] = False
            else:
                user.settings['profile']['two_factor_enabled'] = True
            user.save()
        elif selector == "company":
            formFill = company_Update_form(request.POST, request.FILES, instance=primaryModel)
            if formFill.is_valid():
                formFill.save()
                print("saved tthat shit")
        return redirect("Account")
    return render(request, 'supervisor/settings/settings_account_update.html', variables)
    
@lock
def sup_facility_settings(request, facilityID, selector):
    notifs = checkIfFacilitySelected(request.user)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    facInfoMain = facility_model.objects.get(id=facilityID)
    clientUserProfs = user_profile_model.objects.filter(facilityChoice=facInfoMain)
    facilityInfo = ''

    if selector == 'faci':
        initial_data = {
            'bat_num': facInfoMain.bat_num, 
            'total_ovens': facInfoMain.total_ovens, 
            'facility_name': facInfoMain.facility_name, 
            'county': facInfoMain.county, 
            'estab_num': facInfoMain.estab_num, 
            'equip_location': facInfoMain.equip_location, 
            'address': facInfoMain.address, 
            'state': facInfoMain.state, 
            'district': facInfoMain.district, 
            'bat_height': facInfoMain.bat_height, 
            'bat_height_label': facInfoMain.bat_height_label, 
            'bat_main': facInfoMain.bat_main, 
            'bat_lids': facInfoMain.bat_lids, 
            'city': facInfoMain.city,
            'is_battery': facInfoMain.is_battery,
            'zipcode': facInfoMain.zipcode
        }
        facilityInfo = bat_info_form(initial=initial_data)
    elif selector in ['batd', 'noti', 'main']:
        facilityInfo = request.user.user_profile.settings['facilities'][str(facilityID)]

    userProfileQuery = user_profile_model.objects.all()
    accountData = userProfileQuery.get(user__id=request.user.id)
    userCompany = accountData.company
    listOfEmployees = userProfileQuery.filter(~Q(position="client"), company=userCompany, )
    active_registrations = len(listOfEmployees.filter(company__braintree__settings__account__status='active'))

    dateStart = "1900-01-01"
    dateStart = datetime.strptime(dateStart, "%Y-%m-%d")
        
    if request.method == "POST":
        answer = request.POST
        if 'facilityInfoSave' in answer:
            form = bat_info_form(answer, instance=facInfoMain)
            if form.is_valid():
                form.save()
                return redirect('selectedFacilitySettings', facilityID, 'main')
        elif 'batteryDashSave' in answer:
            if not unlock:
                accountData.settings['facilities'][str(facInfoMain.id)]['settings'] = {}
                batDashSettings = accountData.settings['facilities'][str(facInfoMain.id)]['settings']
                progressOptions = ['progressDaily', 'progressWeekly', 'progressMonthly', 'progressQuarterly', 'progressAnnually']
                if 'progressBar' in answer.keys():
                    if answer['progressBar'] == 'true':
                        batDashSettings['progressBar'] = {}
                        for progOpt in progressOptions:
                            progInput = False
                            if progOpt in answer.keys():
                                if answer[progOpt] == 'true':
                                    progInput = True
                            batDashSettings['progressBar'][progOpt] = progInput
                else:
                    batDashSettings['progressBar'] = False
                if 'graphs' in answer.keys():
                    if answer['graphs'] == 'true':
                        batDashSettings['graphs'] = {}
                        graphOptions = ['charges', 'doors', 'lids', 'graph90dayPT']
                        if answer['graphFrequency'] == 'dates':
                            batDashSettings['graphs']['graphFrequencyData'] = {
                                'frequency': answer['graphFrequency'],
                                'dates': {
                                    'graphStart': answer['graphStart'],
                                    'graphStop': answer['graphStop']
                                }
                            }
                        else:
                            batDashSettings['graphs']['graphFrequencyData'] = {
                                'frequency': answer['graphFrequency'],
                                'dates': False
                            }
                        batDashSettings['graphs']['dataChoice'] = {}
                        for graphOpt in graphOptions:
                            graphInput = False
                            if graphOpt in answer.keys():
                                if answer[graphOpt] == 'true':
                                    graphInput = True
                            batDashSettings['graphs']['dataChoice'][graphOpt] = {'show': graphInput, 'type': 'bar'}
                else:
                    batDashSettings['graphs'] = False
                if 'correctiveActions' in answer.keys():
                    if answer['correctiveActions'] == 'true':
                        batDashSettings['correctiveActions'] = True
                else:
                    batDashSettings['correctiveActions'] = False
                if 'infoWeather' in answer.keys():
                    if answer['infoWeather'] == 'true':
                        batDashSettings['infoWeather'] = True
                else:
                    batDashSettings['infoWeather'] = False
                if '90dayPT' in answer.keys():
                    if answer['90dayPT'] == 'true':
                        batDashSettings['90dayPT'] = True
                else:
                    batDashSettings['90dayPT'] = False
                if 'contacts' in answer.keys():
                    if answer['contacts'] == 'true':
                        batDashSettings['contacts'] = True
                else:
                    batDashSettings['contacts'] = False
                print(batDashSettings)
            else:
                accountData.settings['dashboard'][str(facInfoMain.id)]['batteryDash'] = True
            A = accountData
            A.save()
            return redirect('selectedFacilitySettings', facilityID, 'main')
        elif 'notifSettingsForm' in answer:
            accountData.settings['facilities'][str(facilityID)]['notifications'] = {}
            notificatoinSettingsData = accountData.settings['facilities'][str(facilityID)]['notifications']
            notifOptions = ['compliance', 'deviations', 'submitted', '10_day_pt', '5_day_pt']
            for notifOp in notifOptions:
                methodPlusOpt = True if f"{notifOp}-methodplus" in answer.keys() else False
                emailOpt = True if f"{notifOp}-email" in answer.keys() else False
                smsOpt = True if f"{notifOp}-sms" in answer.keys() else False
                notificatoinSettingsData[notifOp] = {
                    "methodplus": methodPlusOpt,
                    "email": emailOpt, 
                    "sms": smsOpt
                }
            A = accountData
            A.save()
            return redirect('selectedFacilitySettings', facilityID, 'main')
        elif 'defaultBatteryDash' in answer:
            if answer['defaultBatteryDash'] == 'true':
                A  = accountData
                A.settings['facilities'] = json.loads(json.dumps(setDefaultSettings(accountData, request.user.username)['facilities']))
                A.save()
                return redirect('selectedFacilitySettings', facilityID, 'main')
        elif 'defaultNotif' in answer:
            if answer['defaultNotif'] == 'true':
                A  = accountData
                A.settings['facilities'][str(facilityID)]['notifications'] = json.loads(json.dumps(defaultNotifications))
                A.save()
                return redirect('selectedFacilitySettings', facilityID, 'main')
        elif 'cancelAccount' in answer:
            print("hello")
            clientAccountProf = get_object_or_404(user_profile_model, id=int(answer['registerID']))
            clietnAccount = clientAccountProf.user
            print(clietnAccount)
            clientAccountProf.delete()
            clietnAccount.delete()


            
    return render(request, 'supervisor/settings/selected_facility_settings.html',{
        'notifs': notifs,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facilityID': facilityID,
        'facilityIDString': str(facilityID),
        'facilityInfo': facilityInfo,
        'facInfoMain': facInfoMain,
        'clientUserProfs': clientUserProfs,
        'selector': selector,
        'accountData': accountData,
        'listOfEmployees': listOfEmployees,
        'active_registrations': active_registrations,
        'userProfileQuery': userProfileQuery,
        'dashDict': json.loads(json.dumps(dashDictOptions))
    })