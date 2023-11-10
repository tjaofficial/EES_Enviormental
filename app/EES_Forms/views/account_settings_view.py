from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import braintree
from ..utils import checkIfFacilitySelected, setUnlockClientSupervisor, braintreeGateway, getCompanyFacilities
from ..models import user_profile_model, company_model
import datetime
import json

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
    }
    
    if selector == 'subscription':
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
        accountData = user_profile_model.objects.get(user__username=request.user.username)
        customerId = accountData.company.customerID
        customer = gateway.customer.find(customerId)
        cardsOnFile = customer.credit_cards
        print(request.POST)
        variables['customer'] = customer
        variables['cardsOnFile'] = cardsOnFile
        link = "supervisor/settings/braintree/select_payment.html"
    elif selector == "review":
        link = "supervisor/settings/braintree/select_review.html"
        
    return render(request, link, variables)

@lock
def sup_account_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    
    facility = 'supervisor'
    sortedFacilityData = getCompanyFacilities(request.user.username)
    userProfileQuery = user_profile_model.objects.all()
    accountData = userProfileQuery.get(user__username=request.user.username)
    userCompany = accountData.company
    listOfEmployees = userProfileQuery.filter(~Q(id=accountData.id), company=userCompany)
    print(sortedFacilityData)
    cardSubscription = False
    try:
        customerId = accountData.company.customerID
        gateway = braintreeGateway()
        customer = gateway.customer.find(customerId)
        print(customer)
        dateStart = "1900-01-01"
        dateStart = datetime.datetime.strptime(dateStart, "%Y-%m-%d")
        for card in customer.credit_cards:
            for sub in card.subscriptions:
                if sub.status == 'Active':
                    finished = True
                    cardSubscription = {
                        'first_billing_date': sub.first_billing_date,
                        'billing_day_of_month': sub.billing_day_of_month,
                        'billing_period_start_date': sub.billing_period_start_date,
                        'billing_period_end_date': sub.billing_period_end_date, #(day before the billing day in the next month)
                        'next_billing_date': sub.next_billing_date,
                        'plan_id': sub.plan_id,
                        'price': sub.price,
                        'status': sub.status,
                        'last_4': card.last_4,
                        'card_type': card.card_type,
                        'cardholder': card.cardholder_name,
                    }
                    break
            if finished:
                break    
                # .transactions[0] #this is a list# 
                    # id
                    # amount
                    # plan_id
                    # .credit_card_details
                        # token
                        # last_4
                        # card_type
            #     print(sub.first_billing_date)
            #     break
            # break
    except:
        cardSubscription = ''
    return render(request, 'supervisor/settings/sup_account.html',{
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'sortedFacilityData': sortedFacilityData,
        'facility': facility,
        'accountData': accountData,
        'cardSubscription': cardSubscription,
        'notifs': notifs,
        'listOfEmployees': listOfEmployees
    })
    
@lock
def sup_card_update(request, facility, action):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock = setUnlockClientSupervisor(request.user)[0]
    client = setUnlockClientSupervisor(request.user)[1]
    supervisor = setUnlockClientSupervisor(request.user)[2]
    if unlock:
        return redirect('IncompleteForms', facility)
    accountData = user_profile_model.objects.get(user__username=request.user.username)
    gateway = braintreeGateway()
    customerId = accountData.company.customerID
    if action != "add":
        token = accountData.company.payment_method_token
        payment_method = gateway.payment_method.find(token)
    variables = {
            'supervisor': supervisor, 
            "client": client, 
            'unlock': unlock,
            'facility': facility,
            'notifs': notifs,
            "action": action,
        }
    
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
    def addCard(token):
        newCard = gateway.payment_method.update(token, {
            "billing_address": {
                "street_address": request.POST['address1'],
                "extended_address": request.POST['address2'],
                "locality": request.POST['city'],
                "region": request.POST['state'],
                "postal_code": request.POST['postalCode'],
                "options": {
                    "update_existing": True
                }
            },
            'cardholder_name': request.POST['nameOnCard'],
            'number':  request.POST['card-number'],
            'expiration_date': request.POST['expiration-date'],
            'cvv': request.POST['cvv'],
            "options": {
                'make_default': True,
                'verify_card': True,
                'skip_advanced_fraud_checking': False
            }
        })
        if newCard.is_success:
            transaction = newCard.is_success
        else:
            transaction = newCard.errors.deep_errors
        return transaction
        
    if action in {"update","change"}:
        customer = gateway.customer.find(customerId)
        # customer = gateway.customer.find("the_customer_id")
        # customer.payment_methods # array of braintree.PaymentMethod instances
        template = "supervisor/settings/braintree/sup_cardUpdate.html"
        variables['customer'] = customer
        variables['token'] = token
        variables['payment_method'] = payment_method
    elif action == "add":
        if customerId is None:
            client_token = gateway.client_token.generate()
        else:
            client_token = gateway.client_token.generate({
                "customer_id": customerId
            })
        customer = gateway.customer.find(customerId)
        # customer = gateway.customer.find("the_customer_id")
        # customer.payment_methods # array of braintree.PaymentMethod instances
        template = "supervisor/settings/braintree/sup_cardAdd.html"
        variables['customer'] = customer
        variables['client_token'] = client_token
        
    elif action == "cancel":
        template = "supervisor/settings/braintree/sup_cancelSub.html"
        variables['token'] = token
        variables['payment_method'] = payment_method
         
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
            addCard(token)
            print(addCard(token))
        elif cancelSub:
            if request.POST['cancel'] == 'cancel':
                subscriptions = payment_method.subscriptions
                for sub in subscriptions:
                    if sub.status == "Active":
                        subscriptionID = sub.id
                result = gateway.subscription.cancel(subscriptionID)
            print('SUBSCRIPTION CANCELLED')
    
    return render (request, template, variables)