from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import braintree
from ..utils import checkIfFacilitySelected, setUnlockClientSupervisor, braintreeGateway, getCompanyFacilities, checkIfMoreRegistrations
from ..models import user_profile_model, company_model, User, braintree_model
from ..forms import CreateUserForm, user_profile_form, company_form
import datetime
import json
from django.contrib.auth.forms import UserCreationForm

lock = login_required(login_url='Login')

@lock
def sup_select_subscription(request, facility, selector):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    gateway = braintreeGateway()
    
    variables = {
        'notifs': notifs,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'selector': selector
    }
    
    if selector == 'subscription':
        plans = gateway.plan.all()
        cPlan = []
        for plan in plans:
            oPlan = {
                'pid': plan.id,
                'billingDOM': plan.billing_day_of_month,
                'currency_iso_code': plan.currency_iso_code,
                'description': plan.description.split("\n"),
                'Customizable_Forms': 'Customizable Forms',
                'Real_time_Data_Entry': 'Real-time Data Entry',
                'Multimedia_Integration': 'Multimedia Integration',
                'Advanced_Reporting': 'Advanced Reporting',
                'Collaborative_Workflows': 'Collaborative Workflows',
                'Security_and_Compliance': 'Security and Compliance',
                'Offline_Accessibility': 'Offline Accessibility',
                'name': plan.name,
                'price': plan.price
                }
            cPlan.append(oPlan)
        cPlan.sort(key=lambda d: d['price'])
        print(cPlan[0]['description'])
        variables['planList'] = cPlan
        link = "supervisor/settings/braintree/select_subscription.html"
    elif selector == "registration":
        plans = gateway.plan.all()
        for iPlans in plans:
            print(iPlans)
            if iPlans.id == request.POST['planId']:
                selectedPlan = iPlans
        print(request.POST)
        variables['selectedPlan'] = selectedPlan
        link = "supervisor/settings/braintree/select_registration_amount.html"
    elif selector == "payment":
        print(request.POST)
        user = request.user
        accountData = user_profile_model.objects.get(user__id=user.id)
        customerId = accountData.company.braintree.customerID
    
        if customerId and customerId != 'none':
            customer = gateway.customer.find(customerId)
        else:
            newCustomer = gateway.customer.create({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "company": accountData.company.company_name,
                "email": user.email,
                "phone": accountData.phone
            })
            if newCustomer.is_success:
                userCompany = company_model.objects.get(id=accountData.company.id)
                userCompany.braintree.customerID = newCustomer.customer.id
                userCompany.save()
                customer = gateway.customer.find(userCompany.braintree.customerID)
            else:
                for i in newCustomer.errors.deep_errors:
                    print(i.code)
                    if i.code == "81724":
                        print("Duplicate card exists.")
        cardsOnFile = customer.credit_cards
        print(cardsOnFile)
        cardData = request.POST.get('payNonce', False)
        dataTemplateUse = request.POST
        if 'payNonce' in request.POST.keys():
            cardData = gateway.payment_method_nonce.find(request.POST['payNonce'])
        else:
            cardData = False
        plans = gateway.plan.all()
        for plan in plans:
            if plan.id == request.POST['planId']:
                planDetails = plan
        addRegistrationCost = format(int(request.POST['seats'])*75, '.2f')
        totalCost = format(float(planDetails.price) + float(addRegistrationCost), '.2f')
        # if len(cardsOnFile) < 0 or cardData:
        #     dataTemplateUse = request.POST
        # else:
        #     dataTemplateUse = False
        variables['dataTemplateUse'] = dataTemplateUse
        variables['customer'] = customer
        variables['cardsOnFile'] = cardsOnFile
        variables['selectedPlan'] = request.POST['planId']
        variables['seats'] = request.POST['seats']
        variables['cardData'] = cardData
        variables['totalData']  = request.POST
        variables['planDetails'] = planDetails
        variables['addRegistrationCost'] = addRegistrationCost
        variables['totalCost'] = totalCost
        link = "supervisor/settings/braintree/select_payment.html"
    elif selector == "receipt":
        print(request.POST)
        user = request.user
        accountData = user_profile_model.objects.get(user__username=user.username)
        customerId = accountData.company.braintree.customerID
        plans = gateway.plan.all()
        for plan in plans:
            if plan.id == request.POST['planId']:
                planDetails = plan
        addRegistrationCost = format(int(request.POST['seats'])*75, '.2f')
        totalCost = format(float(planDetails.price) + float(addRegistrationCost), '.2f')
        if request.POST['paymentSelected'][5:] == "new":
            updateCustomer = gateway.customer.update(customerId, {
                "payment_method_nonce": request.POST['payNonce'],
                'credit_card':{ # A credit or debit payment method.
                    'billing_address': { # A billing address associated with a specific credit card. The maximum number of addresses per customer is 50. - 
                        'company': accountData.company.company_name,   # str - Company name. Maximum 255 characters.
                        'street_address': request.POST['address1'],   # str - The street address. Maximum 255 characters.  
                        'extended_address': request.POST['address2'],   # str - The extended address information—such as apartment or suite number. 255 character maximum.
                        'locality': request.POST['city'],    # str - The locality/city. Maximum 255 characters.
                        'postal_code': request.POST['zipCode'],    # str - The postal code. Postal code must be a string of 4-9 alphanumeric characters, optionally separated by a dash or a space. Spaces and hyphens are ignored.
                        'region': request.POST['state'],    # str - The state or province. Maximum 255 characters.
                        'country_code_alpha2': 'US',    # str - The ISO 3166-1 alpha-2 country code specified in an address. The gateway only accepts specific alpha-2 values.
                    },    
                    'cardholder_name': request.POST['nameOnCard'],    # str - The name associated with the credit card. Must be less than or equal to 175 characters.
                    'options':{ # Optional values that can be passed with a request. - 
                        'fail_on_duplicate_payment_method': True,    # bool - If this option is passed and the same payment method has already been added to the Vault for any customer, the request will fail. This option will be ignored for PayPal, Pay with Venmo, Apple Pay, Google Pay, and Samsung Pay payment methods.
                        'make_default': True,    # bool - This option makes the specified payment method the default for the customer.
                        'skip_advanced_fraud_checking': False,    # boolean - If the payment method is a credit card, prevents the verification from being evaluated as part of Premium Fraud Management Tools checks. Use with caution – once you've skipped checks for a verification, it is not possible to run them retroactively.:     #  - 
                        'verify_card': True,   # bool - If the payment method is a credit card, this option prompts the gateway to verify the card's number and expiration date. It also verifies the AVS and CVV information if you've enabled AVS and CVV rules.:     #  - NOTE Braintree strongly recommends verifying all cards before they are stored in your Vault by enabling card verification for your entire account in the Control Panel. In some cases, cardholders may see a temporary authorization on their account after their card has been verified. The authorization will fall off the cardholder's account within a few days and will never settle.:     #  - Only returns a CreditCardVerification result if verification runs and is unsuccessful.
                    }     
                } ,    
            })
            
            if not updateCustomer.is_success:
                print(updateCustomer)
                print('ERROR UPDATING CUSTOMER')
                for i in updateCustomer.errors.deep_errors:
                    print(i.code)
                    if i.code == "81724":
                        print("Duplicate card exists.")
                        
            vaultPaymentToken = updateCustomer.customer.payment_methods[0].token
            addSubsriptionResult = gateway.subscription.create({
                "payment_method_token": vaultPaymentToken,
                "plan_id": request.POST['planId']
            })
        else:
            vaultPaymentToken = accountData.company.braintree.payment_method_token
            addOnEdits = {
                "payment_method_token": vaultPaymentToken,
                "plan_id": request.POST['planId']
            }
            if request.POST['seats'] == 0:
                addOnEdits["add_ons"] = {
                    "remove": ["86gr"]
                }
            else:
                addOnEdits["add_ons"] = {
                    "update": [{
                        "existing_id": "86gr",
                        "quantity": request.POST['seats']
                    }]
                }
            addSubsriptionResult = gateway.subscription.create(addOnEdits)
    
        userComp = company_model.objects.filter(company_name=accountData.company.company_name)
        if userComp.exists():
            userComp = userComp[0]
        else:
            print("No Compnay has been entered for user profile information")
            
        if not addSubsriptionResult.is_success:
            print('ERROR CREATING NEW SUBSCRIPTION')
            for i in addSubsriptionResult.errors.deep_errors:
                print(i)
        else:
            userComp.braintree.payment_method_token = vaultPaymentToken
            userComp.braintree.subID = addSubsriptionResult.subscription.transactions[0].subscription_id
            userComp.save()
            print('MADE IT TO FUCKING SAVE')

        variables['totalData']  = request.POST
        variables['planDetails'] = planDetails
        variables['addRegistrationCost'] = addRegistrationCost
        variables['totalCost'] = totalCost
        link = "supervisor/settings/braintree/select_receipt.html"
        
    return render(request, link, variables)

@lock
def sup_account_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    braintreeData = braintree_model.objects.filter(user__id=request.user.id)
    if braintreeData.exists():
        braintreeData = braintreeData.get(user__id=request.user.id)
    else:
        print('handle if there is no braintree entry')
        
    facility = 'supervisor'
    sortedFacilityData = getCompanyFacilities(request.user.username)
    userProfileQuery = user_profile_model.objects.all()
    accountData = userProfileQuery.get(user__id=request.user.id)
    userCompany = accountData.company
    listOfEmployees = userProfileQuery.filter(~Q(position="client"), company=userCompany, )
    active_registrations = len(listOfEmployees.filter(company__braintree__status='active'))

    dateStart = "1900-01-01"
    dateStart = datetime.datetime.strptime(dateStart, "%Y-%m-%d")
        
    if request.method == "POST":
        data = request.POST
        if 'facilitySelect' in data.keys():
            if data['facilitySelect'] != '':
                return redirect('sup_dashboard', data['facilitySelect'])
        else:
            print(data)
            selectedRegister = userProfileQuery.get(id=int(data['registerID']))
            selectedRegister.company.braintree.status = "active"
            selectedRegister.save()
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
        'accountData': accountData,
        'active_registrations': active_registrations,
        'braintreeData': braintreeData
    })
    
@lock
def sup_card_update(request, facility, action, planId=False, seats=False):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    accountData = user_profile_model.objects.get(user__id=request.user.id)
    gateway = braintreeGateway()
    customerId = accountData.company.braintree.customerID
    if action[0:3] != "add":
        token = accountData.company.braintree.payment_method_token
        payment_method = gateway.payment_method.find(token)
    variables = {
            'supervisor': supervisor, 
            "client": client, 
            'unlock': unlock,
            'facility': facility,
            'notifs': notifs,
            "action": action,
        }
    customer = gateway.customer.find(customerId)
    def updateCardAddress(token):
        updateCard = gateway.payment_method.update(token, {
            "billing_address": {
                "street_address": request.POST['address1'],
                "extended_address": request.POST['address2'],
                "locality": request.POST['city'],
                "region": request.POST['state'],
                "postal_code": request.POST['postalCode'],
                "options": {
                    "update_existing": True
                }
            }
        })
        
        if updateCard.is_success:
            transaction = updateCard.is_success
        else:
            transaction = updateCard.errors.deep_errors
        return transaction
    def addCard(customerId, token):
        print('hello')
        
        
        
        
        
        
        
        # updateCard = gateway.payment_method.update(token, {
        #     "billing_address": {
        #         "street_address": request.POST['address1'],
        #         "extended_address": request.POST['address2'],
        #         "locality": request.POST['city'],
        #         "region": request.POST['state'],
        #         "postal_code": request.POST['postalCode'],
        #         "options": {
        #             "update_existing": True
        #         }
        #     },
        #     'cardholder_name': request.POST['nameOnCard'],
        #     'number': request.POST['nameOnCard'],
        #     'expiration_date': request.POST['nameOnCard'],
        #     'cvv': request.POST['nameOnCard'], 
        #     'options': {
        #         'make_default': True,
        #         'verify_card': True
        #     }
        # })
        
        
        
        
        # result = gateway.payment_method_nonce.create(token)
        # nonce = result.payment_method_nonce.nonce
        # newerCard = gateway.payment_method.create({
        #     "customer_id": customerId,
        #     "payment_method_nonce": nonce,
        #     "options": {
        #         "verify_card": True
        #     }
        # })
        
        
        # newCard = gateway.payment_method.create(token, {
        #     "billing_address": {
        #         "street_address": request.POST['address1'],
        #         "extended_address": request.POST['address2'],
        #         "locality": request.POST['city'],
        #         "region": request.POST['state'],
        #         "postal_code": request.POST['postalCode'],
        #         "options": {
        #             "update_existing": True
        #         }
        #     },
        #     'cardholder_name': request.POST['nameOnCard'],
        #     'number':  request.POST['card-number'],
        #     'expiration_date': request.POST['expiration-date'],
        #     'cvv': request.POST['cvv'],
        #     "options": {
        #         'make_default': True,
        #         'verify_card': True,
        #         'skip_advanced_fraud_checking': False
        #     }
        # })
        # if newCard.is_success:
        #     transaction = newCard.is_success
        # else:
        #     transaction = newCard.errors.deep_errors
        # return transaction
        
    if action in {"update","change"}:
        template = "supervisor/settings/braintree/sup_cardUpdate.html"
        variables['customer'] = customer
        variables['token'] = token
        variables['payment_method'] = payment_method
    elif action[0:3] == "add":
        print("maide it through the second add")
        print(request.POST)
        if customerId and customerId != 'none':
            client_token = gateway.client_token.generate({
                "customer_id": customerId
            })
        else:
            client_token = gateway.client_token.generate()
        customer = gateway.customer.find(customerId)
        # customer = gateway.customer.find("the_customer_id")
        # customer.payment_methods # array of braintree.PaymentMethod instances
        template = "supervisor/settings/braintree/sup_cardAdd.html"
        variables['customer'] = customer
        variables['client_token'] = client_token
        variables['pId'] = planId
        variables['seats'] = seats
    elif action == "cancel":
        subID = accountData.company.braintree.subID
        sub = gateway.subscription.find(subID)
        if sub.status == "Active":
            activeSub = gateway.subscription.find(subID)
            billing_period_end_date = activeSub.billing_period_end_date
        template = "supervisor/settings/braintree/sup_cancelSub.html"
        variables['token'] = token
        variables['payment_method'] = payment_method
        variables['billing_period_end_date'] = billing_period_end_date
         
    if request.method == "POST":
        updateAddress = request.POST.get('updateAddress', False)
        newCard = request.POST.get('newCard', False)
        cancelSub = request.POST.get('cancelSub', False)
        if updateAddress:
            updateCardAddress(token)
            company = company_model.objects.get(id=accountData.company.id)
            company.address = request.POST['address1'] + ", " + request.POST['address2']
            company.city = request.POST['city']
            company.state = request.POST['state']
            company.zipcode = request.POST['postalCode']
            company.save()
            print("UPDATED ADDRESS")
            return redirect('Account', facility)
        elif newCard:
            print('new CArd')
        elif cancelSub:
            if request.POST['cancel'] == 'cancel':
                subID = accountData.company.subID
                cancelResult = gateway.subscription.cancel(subID)
                print(cancelResult)
                print('SUBSCRIPTION CANCELLED')
                return redirect("Account", facility)
    
    return render (request, template, variables)

@lock
def sup_update_account(request, facility, selector):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    facility = 'supervisor'
    user = user_profile_model.objects.get(user__id=request.user.id)
    variables = {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'notifs': notifs,
        'selector': selector
    }
    if selector == "account":
        primaryModel = User.objects.get(id=request.user.id)
        initial_data = {
            'username': user.user.username,
            'first_name': user.user.first_name,
            'last_name': user.user.last_name,
            'email': user.user.email,
            'cert_date': user.cert_date,
            'phone': user.phone,
            'certs': user.certs,
            'profile_picture': user.profile_picture,
        }
        primaryForm = CreateUserForm(initial=initial_data)
        secondaryForm = user_profile_form(initial=initial_data)
        variables['secondaryForm'] = secondaryForm
    elif selector == "company":
        primaryModel = company_model.objects.get(id=user.company.id)
        initial_data = {
            'company_name': primaryModel.company_name,
            'address': primaryModel.address,
            'city': primaryModel.city,
            'state': primaryModel.state,
            'zipcode': primaryModel.zipcode,
            'phone': primaryModel.phone,
        }
        primaryForm = company_form(initial=initial_data)
    
    variables['primaryForm'] = primaryForm
    if request.method == 'POST':
        print(request.POST)
        dataFromForm = request.POST
        if selector == "account":
            primaryModel.first_name = dataFromForm['first_name']
            primaryModel.last_name = dataFromForm['last_name']
            primaryModel.username = dataFromForm['username']
            primaryModel.email = dataFromForm['email']
            user.cert_date = dataFromForm['cert_date']
            user.phone = dataFromForm['phone']
            user.save()
        elif selector == "company":
            primaryModel.company_name = dataFromForm['company_name']
            primaryModel.address = dataFromForm['address']
            primaryModel.city = dataFromForm['city']
            primaryModel.state = dataFromForm['state']
            primaryModel.zipcode = dataFromForm['zipcode']
            primaryModel.phone = dataFromForm['phone']
            
        primaryModel.save()
        return redirect("Account", facility)

    return render(request, 'supervisor/settings/settings_account_update.html', variables)

@lock
def sup_change_subscription(request, facility):   
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    facility = 'supervisor'
    user = user_profile_model.objects.get(user__id=request.user.id)
    subID = user.company.braintree.subID
    gateway = braintreeGateway()
    activeSub = gateway.subscription.find(subID)
    plans = gateway.plan.all()
    cPlan = []
    print(plans[0])
    for plan in plans:
        oPlan = {
            'pid': plan.id,
            'billingDOM': plan.billing_day_of_month,
            'currency_iso_code': plan.currency_iso_code,
            'description': plan.description.split("\n"),
            'Customizable_Forms': 'Customizable Forms',
            'Real_time_Data_Entry': 'Real-time Data Entry',
            'Multimedia_Integration': 'Multimedia Integration',
            'Advanced_Reporting': 'Advanced Reporting',
            'Collaborative_Workflows': 'Collaborative Workflows',
            'Security_and_Compliance': 'Security and Compliance',
            'Offline_Accessibility': 'Offline Accessibility',
            'name': plan.name,
            'price': plan.price
            }
        cPlan.append(oPlan)
    cPlan.sort(key=lambda d: d['price'])
    return render(request, 'supervisor/settings/braintree/sup_changeSub.html', {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'notifs': notifs,
        'planList': cPlan,
        'activeSub': activeSub
    })
  
@lock  
def sup_billing_history(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    facility = 'supervisor'
    user = user_profile_model.objects.get(user__id=request.user.id)
    subID = user.company.braintree.subID
    gateway = braintreeGateway()
    activeSub = gateway.subscription.find(subID)
    return render(request, 'supervisor/settings/braintree/sup_billing_history.html', {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'notifs': notifs,
        'activeSub': activeSub
    })