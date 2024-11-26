from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Q # type: ignore
from ..utils import parsePhone, get_braintree_query, setDefaultSettings, dashDictOptions, checkIfFacilitySelected, setUnlockClientSupervisor, braintreeGateway, getCompanyFacilities, defaultBatteryDashSettings, defaultNotifications
from ..models import user_profile_model, company_model, User, braintree_model, braintreePlans, bat_info_model, account_reactivation_model
from ..forms import CreateUserForm, user_profile_form, company_Update_form, bat_info_form
import datetime
import braintree # type: ignore
import json


lock = login_required(login_url='Login')

@lock
def sup_select_subscription(request, facility, selector):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    user = request.user
    gateway = braintreeGateway()
    
    variables = {
        'notifs': notifs,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'selector': selector
    }
    plans = braintreePlans.objects.all()
    print(selector[14:])
    if selector == 'subscription':
        cPlan = []
        for plan in plans:
            oPlan = {
                'pid': plan.id,
                'description': plan.description.split("\n"),
                'name': plan.name,
                'price': plan.price,
                'Customizable_Forms': 'Customizable Forms',
                'Real_time_Data_Entry': 'Real-time Data Entry',
                'Multimedia_Integration': 'Multimedia Integration',
                'Advanced_Reporting': 'Advanced Reporting',
                'Collaborative_Workflows': 'Collaborative Workflows',
                'Security_and_Compliance': 'Security and Compliance',
                'Offline_Accessibility': 'Offline Accessibility',
                }
            cPlan.append(oPlan)
        cPlan.sort(key=lambda d: d['price'])
        print(cPlan[0]['description'])
        variables['planList'] = cPlan
        link = "supervisor/settings/braintree/select_subscription.html"
    elif len(selector) >= 12 and selector[:12] == "registration":
        print('fuking madeit')
        form_data = request.session.get('form_data')
        print(form_data)
        change = False
        if selector[13:] == 'change':
            change = True
        for iPlans in plans:
            if iPlans.id == int(form_data['planId']):
                selectedPlan = iPlans
        variables['selectedPlan'] = selectedPlan
        link = "supervisor/settings/braintree/select_registration_amount.html"
    elif len(selector) >= 7 and selector[:7] == "payment":
        subChange = False
        if selector[8:] == 'subChange':
            subChange = True
        form_data = request.session.get('form_data')
        print(form_data)
        if 'seats' not in request.POST.keys():
            seats = int(form_data['seats'])
            planID = int(form_data['planID'])
        else:
            seats = int(request.POST['seats'])
            planID = int(request.POST['planId'])
        addRegistrationCost = format(seats*75, '.2f')
        accountData = user_profile_model.objects.get(user__id=user.id)
        customerId = accountData.company.braintree.settings['account']['customer_ID']
        for plan in plans:
            if plan.id == planID:
                planDetails = plan
        totalCost = format(float(planDetails.price) + float(addRegistrationCost), '.2f')
        btQuery = braintree_model.objects.get(user=request.user)

        if subChange:
            subChange = {
                'plan_cost': planDetails.price,
                'addRegistrationCost': format(seats*75, '.2f'),
                'total_cost': totalCost,
                'old_total': btQuery.settings['subscription']['price'],
                'due': format(float(totalCost) - float(btQuery.settings['subscription']['price']), '.2f')
            }

        if customerId and customerId != 'none':
            print("check 1")
            customer = gateway.customer.find(customerId)
            print(customer)
            print(customer.payment_methods)
        else:
            print("check 2")
            newCustomer = gateway.customer.create({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "company": accountData.company.company_name,
                "email": user.email,
                "phone": accountData.phone
            })
            if newCustomer.is_success:
                userCompany = company_model.objects.get(id=accountData.company.id)
                userCompany.braintree.settings['account']['customer_ID'] = newCustomer.customer.id
                userCompany.braintree.save()
                userCompany.save()
                customer = gateway.customer.find(userCompany.braintree.settings['account']['customer_ID'])
            else:
                for i in newCustomer.errors.deep_errors:
                    print(i.code)
                    if i.code == "81724":
                        print("Duplicate card exists.")
        cardsOnFile = customer.credit_cards
        print(cardsOnFile)
        dataTemplateUse = request.POST
        variables['dataTemplateUse'] = dataTemplateUse
        variables['customer'] = customer
        variables['cardsOnFile'] = cardsOnFile
        variables['selectedPlan'] = planID
        variables['seats'] = seats
        variables['totalData']  = request.POST
        variables['planDetails'] = planDetails
        variables['addRegistrationCost'] = addRegistrationCost
        variables['totalCost'] = totalCost
        variables['subChange'] = subChange
        link = "supervisor/settings/braintree/select_payment.html"
    elif selector == "receipt":
        print(request.POST)
        form_data = request.session.get('form_data')
        print(form_data)
        seats = form_data['seats']
        accountData = user_profile_model.objects.get(user__username=user.username)
        customerId = accountData.company.braintree.settings['account']['customer_ID']
        for plan in plans:
            if plan.id == int(form_data['planId']):
                planDetails = plan
        addRegistrationCost = format(int(seats)*75, '.2f')
        totalCost = format(float(planDetails.price) + float(addRegistrationCost), '.2f')

        variables['totalData']  = form_data
        variables['planDetails'] = planDetails
        variables['addRegistrationCost'] = addRegistrationCost
        variables['totalCost'] = totalCost
        link = "supervisor/settings/braintree/select_receipt.html"
    
    if request.method == "POST":
        print(request.POST)
        if "subSelect" in request.POST:
            if "form_data" in request.session:
                del request.session['form_data']
            request.session['form_data'] = request.POST
            currentPlanStatus = braintree_model.objects.get(user=request.user).settings['subscription']['status']
            url_addition = "registration"
            if currentPlanStatus == "active":
                url_addition += "-change"
            return redirect('subscriptionSelect', facility, url_addition)
        if "confirmOrder" in request.POST:
            if "form_data" in request.session:
                del request.session['form_data']
            request.session['form_data'] = request.POST
            if request.POST['paymentToken'] == "default":
                btData = braintree_model.objects.get(user=request.user)
                paymentToken = btData.settings['payment_methods']['default']['payment_token']
                request.session['form_data']['paymentToken'] == btData.settings['payment_methods']['default']['payment_token']
                print(paymentToken)
            

            if subChange:
                result = gateway.transaction.sale({
                    "amount": str(subChange['due']),
                    "payment_method_token": paymentToken,
                    "options": {
                        "submit_for_settlement": True
                    }
                })
                if result.is_success:
                    print("Prorated difference charged successfully.")
                else:
                    print(f"Error charging prorated amount: {result.errors.deep_errors}")
                    # send error message and reset the page dont allow to go any further

            addOnEdits = {"plan_id": planDetails.planID}
            if int(seats) == 0:
                print('check 2')
                if btQuery.settings['subscription']['registrations']-2 != 0:
                    addOnEdits["add_ons"] = {
                        "remove": ["86gr"]
                    }
            else:
                if btQuery.settings['subscription']['registrations']-2 != 0:
                    print('check 3')
                    addOnEdits["add_ons"] = {
                        "update": [{
                            "existing_id": "86gr",
                            "quantity": int(seats)
                        }]
                    }
                else:
                    print('check 4')
                    addOnEdits["add_ons"] = {
                        "add": [{
                            "inherited_from_id": "86gr",
                            "quantity": int(seats),
                        }]
                    }
            if btQuery.settings['subscription']['status'] == 'canceled':
                addOnEdits["payment_method_token"] = paymentToken
                result = gateway.subscription.create(addOnEdits)
                btSubId = result.subscription.id
                btBillingDate = result.subscription.next_billing_date
            elif btQuery.settings['subscription']['status'] == 'active':
                result = gateway.subscription.update(btQuery.settings['subscription']['subscription_ID'], addOnEdits)
                btSubId = btQuery.settings['subscription']['subscription_ID']
                btBillingDate = btQuery.settings['subscription']['next_billing_date']
            if result.is_success:
                print("New Subscription created successfully.")
                #else:
                    #cancelSub = gateway.subscription.cancel(userComp.braintree.settings.['subscription']['subscription_ID]')
                btCopy = btQuery
                btSettings = btCopy.settings
                btSettings['subscription']['subscription_ID'] = btSubId
                btSettings['subscription']['plan_id'] = planDetails.planID
                btSettings['subscription']['plan_name'] = planDetails.name
                btSettings['subscription']['price'] = totalCost
                btSettings['subscription']['registrations'] = int(seats) + 2
                btSettings['subscription']['next_billing_date'] = str(btBillingDate)
                btSettings['subscription']['status'] = "active"
                btSettings['account']['status'] = 'active'
                btCopy.save()

                seatsCalc = btSettings['subscription']['registrations']
                mainSupervisorProf = user_profile_model.objects.get(user=request.user)
                userProfileQuery = user_profile_model.objects.filter(~Q(position="client"), company=mainSupervisorProf.company, settings__position__endswith="activate", user__is_active=False)
                if userProfileQuery.exists():
                    x = 2
                    for emp in userProfileQuery:
                        if x <= seatsCalc:
                            empUser = emp.user
                            empUser.is_active = True
                            empUser.save()
                            emp.settings['position'] = emp.settings['position'].replace("-activate", "")
                            emp.save()
                            x += 1
                        else:
                            emp.settings['position'] = emp.settings['position'].replace("-activate", "")
                            emp.save()
                            x += 1
                print('MADE IT TO FUCKING SAVE')
            else:
                print(f"Error creating new subscription: {result.errors.deep_errors}")
                # send error message and reset the page dont allow to go any further

            return redirect('subscriptionSelect', facility, 'receipt')
        if "confirmRegistration" in request.POST:
            print(request.POST)
            seatsPost = request.POST['seats']
            planIDPost = request.POST['planId']

            if change:
                print("check 1")
                braintreeQuery = braintree_model.objects.get(user=request.user)
                #sub right now            
                old_sub = braintreeQuery.settings['subscription']
                # if old_sub['subscription']['status'] != 'canceled':
                if old_sub:
                    old_price = float(old_sub['price'])
                    braintreeSubID = old_sub['subscription_ID']
                else:
                    old_price = 0
                    braintreeSubID = False
                #new sub
                new_sub = plans.get(id=planIDPost)
                seats_price = 75 * int(seatsPost)
                new_price = new_sub.price + int(seats_price)
                if new_price <= old_price:
                    addOnEdits = {"plan_id": new_sub.planID}
                    if int(seatsPost) == 0:
                        print('check 2')
                        if old_sub['registrations']-2 != 0:
                            addOnEdits["add_ons"] = {
                                "remove": ["86gr"]
                            }
                    else:
                        if old_sub['registrations']-2 != 0:
                            print('check 3')
                            addOnEdits["add_ons"] = {
                                "update": [{
                                    "existing_id": "86gr",
                                    "quantity": int(seatsPost)
                                }]
                            }
                        else:
                            print('check 4')
                            addOnEdits["add_ons"] = {
                                "add": [{
                                    "inherited_from_id": "86gr",
                                    "quantity": int(seatsPost),
                                }]
                            }

                    result = gateway.subscription.update(braintreeSubID, addOnEdits)

                    if not result.is_success:
                        print('ERROR CREATING NEW SUBSCRIPTION')
                        for i in result.errors.deep_errors:
                            print(i)
                    else:
                        print(result)
                        btQueryCopy = braintreeQuery
                        btStettings = btQueryCopy.settings
                        btStettings['subscription']['subscription_ID'] = braintreeSubID
                        btStettings['subscription']['plan_id'] = new_sub.planID
                        btStettings['subscription']['plan_name'] = new_sub.name
                        btStettings['subscription']['price'] = new_price
                        btStettings['subscription']['registrations'] = int(seatsPost) + 2
                        btStettings['subscription']['next_billing_date'] = str(datetime.datetime.today().date())
                        btQueryCopy.save()
                        print('MADE IT TO FUCKING SAVE')
                        return redirect('Account', facility)

                    # save/replace old sub in braintree with new sub, hopefully you can keep the same cycle date
                    # update local braintree Settings, use the JSON to set whether or not the 
                else:
                    # go to payment page to pay the differece
                    if "form_data" in request.session:
                        del request.session['form_data']
                    request.session['form_data'] = {"planID": planIDPost, "seats": seatsPost}
                    return redirect('subscriptionSelect', facility, 'payment-subChange')
            else:
                if "form_data" in request.session:
                    del request.session['form_data']
                request.session['form_data'] = {"planID": planIDPost, "seats": seatsPost}
                return redirect('subscriptionSelect', facility, 'payment')

    return render(request, link, variables)

@lock
def sup_account_view(request, facility):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    # if unlock:
    #     return redirect('IncompleteForms', facility)
    braintreeData = get_braintree_query(request.user)
    if supervisor:
        facility = 'supervisor'
    elif unlock:
        facility = 'observer'
    sortedFacilityData = getCompanyFacilities(request.user.username)
    userProfileQuery = user_profile_model.objects.all()
    accountData = userProfileQuery.get(user__id=request.user.id)
    userCompany = accountData.company
    listOfEmployees = userProfileQuery.filter(~Q(position="client"), company=userCompany)
    companyStatus = braintreeData.settings['account']['status']
    current_date = datetime.datetime.today().date()
    end_of_billing_date = datetime.datetime.strptime(braintreeData.settings['subscription']['next_billing_date'], "%Y-%m-%d").date() if braintreeData.settings['subscription'] else False
    if companyStatus == 'active' or companyStatus == 'canceled' and end_of_billing_date and current_date <= end_of_billing_date:
        active_registrations = len(listOfEmployees.filter(user__is_active=True))
    else:
        active_registrations = 0
    print(str(current_date))
    dateStart = "1900-01-01"
    dateStart = datetime.datetime.strptime(dateStart, "%Y-%m-%d")
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
        'accountData': accountData,
        'active_registrations': active_registrations,
        'braintreeData': braintreeData,
        'userProfileQuery': userProfileQuery,
        'today': (current_date, end_of_billing_date),
        'reactivationQuery': reactivationQuery
    })
    
@lock
def sup_card_update(request, facility, action, planId=False, seats=False):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    accountData = user_profile_model.objects.get(user__id=request.user.id)
    gateway = braintreeGateway()
    customerId = accountData.company.braintree.settings['account']['customer_ID']
    if action[0:3] != "add":
        token = accountData.company.braintree.settings['payment_methods']['default']['payment_token'] if accountData.company.braintree.settings['payment_methods'] else False
        payment_method = gateway.payment_method.find(token) if token else False
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
    def addCard(customerId, token, request):
        print('hello')
        result = gateway.payment_method.create({
            "customer_id": customerId,
            "payment_method_nonce": token,
            "billing_address": {
                "street_address": request['address1'],
                "extended_address": request['address2'],
                "locality": request['city'],
                "region": request['state'],
                "postal_code": request['zipCode'],
                'country_code_alpha2': 'US',
            },
        })

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
        if result.is_success:
            transaction = result.is_success
        else:
            transaction = result.errors.deep_errors
        return transaction, result
        
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
        subID = accountData.company.braintree.settings['subscription']['subscription_ID']
        sub = gateway.subscription.find(subID)
        if sub.status == "Active":
            activeSub = sub
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
            newToken = request.POST['payNonce']
            print('new CArd')
            transaction, newCardDetails = addCard(customerId, newToken, request.POST)
            print(transaction)
            print(newCardDetails)
            print(newCardDetails.payment_method.card_type)
            braintreeQuery = braintree_model.objects.get(user=request.user)
            count = 1
            cardKeyList = braintreeQuery.settings["payment_methods"].keys()
            print(cardKeyList)
            if len(cardKeyList) > 1:
                for cardKey in cardKeyList:
                    if cardKey == "default":
                        continue
                    elif str(count) in cardKeyList:
                        count += 1
                        continue
                    else:
                        print("save new card: " + count )
                        newCardNewKey = str(count)
            else:
                newCardNewKey = "1"
            braintreeQuery.settings["payment_methods"][newCardNewKey] = {
                "type": newCardDetails.payment_method.card_type.lower(),
                "card_name": newCardDetails.payment_method.cardholder_name,
                "payment_token": newToken,
                "last_4": newCardDetails.payment_method.last_4,
                "exp_month": newCardDetails.payment_method.expiration_month,
                "exp_year": newCardDetails.payment_method.expiration_year
            }
            A = braintreeQuery
            print(A)
            A.save()
            if 'form_data' in request.session:
                del request.session['form_data']
            request.session['form_data'] = {"planID": request.POST['planId'], "seats": request.POST['seats']}
            return redirect('subscriptionSelect', facility, 'payment')
        elif cancelSub:
            if request.POST['cancel'] == 'cancel':
                cancelResult = gateway.subscription.cancel(subID)
                print(cancelResult)
                print('SUBSCRIPTION CANCELLED')
                braintreeUpdate = accountData.company.braintree
                braintreeUpdate.settings['account']['status'] = 'canceled'
                braintreeUpdate.settings['subscription']['status'] = 'canceled'
                if braintreeUpdate.settings['past_subscriptions']:
                    new_key = len(braintreeUpdate.settings['past_subscriptions']) + 1
                    braintreeUpdate.settings['past_subscriptions'][new_key] = {
                        "subscription_ID": subID,
                        "start_date": activeSub.created_at,
                        "end_date": billing_period_end_date
                    }
                braintreeUpdate.save()
                return redirect("Account", facility)
    
    return render (request, template, variables)

@lock
def sup_update_account(request, facility, selector):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if supervisor:
        facility = 'supervisor'
    elif unlock:
        facility = 'observer'
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
            'phone': parsePhone(user.phone),
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
            'phone': parsePhone(primaryModel.phone),
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
            user.save()
        elif selector == "company":
            primaryModel.company_name = dataFromForm['company_name']
            primaryModel.address = dataFromForm['address']
            primaryModel.city = dataFromForm['city']
            primaryModel.state = dataFromForm['state']
            primaryModel.zipcode = dataFromForm['zipcode']
            primaryModel.phone = parsePhone(dataFromForm['phone'])
            
        primaryModel.save()
        return redirect("Account", facility)

    return render(request, 'supervisor/settings/settings_account_update.html', variables)

@lock
def sup_change_subscription(request, facility):   
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    gateway = braintreeGateway()
    if unlock:
        return redirect('IncompleteForms', facility)
    facility = 'supervisor'
    user = user_profile_model.objects.get(user__id=request.user.id)
    if user.company.braintree.settings['subscription']:
        subID = user.company.braintree.settings['subscription']['subscription_ID']
        activeSub = gateway.subscription.find(subID)
    else:
        subID = False
        activeSub = False
    plans = braintreePlans.objects.all()
    cPlan = []
    for plan in plans:
        oPlan = {
            'pid': plan.id,
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
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    if unlock:
        return redirect('IncompleteForms', facility)
    facility = 'supervisor'
    user = user_profile_model.objects.get(user__id=request.user.id)
    # subID = user.company.braintree.settings['subscription']['subscription_ID']
    gateway = braintreeGateway()
    collection = gateway.transaction.search(
        braintree.TransactionSearch.customer_id == user.company.braintree.settings['account']['customer_ID']
    )
    return render(request, 'supervisor/settings/braintree/sup_billing_history.html', {
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'notifs': notifs,
        'collection': collection
    })
    
@lock
def sup_facility_settings(request, facility, facilityID, selector):
    notifs = checkIfFacilitySelected(request.user, facility)
    unlock, client, supervisor = setUnlockClientSupervisor(request.user)
    braintreeData = braintree_model.objects.filter(user__id=request.user.id)
    if braintreeData.exists():
        braintreeData = braintreeData.get(user__id=request.user.id)
    else:
        print('handle if there is no braintree entry')
    facInfoMain = bat_info_model.objects.get(id=facilityID)
    #userProf = user_profile_model.objects.get(user__id=request.user.id)
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
            'is_battery': facInfoMain.is_battery
        }
        facilityInfo = bat_info_form(initial=initial_data)
    elif selector in ['batd', 'noti', 'main']:
        facilityInfo = facInfoMain.settings



    if supervisor:
        facility = 'supervisor'
    elif unlock:
        facility = 'observer'
    userProfileQuery = user_profile_model.objects.all()
    accountData = userProfileQuery.get(user__id=request.user.id)
    userCompany = accountData.company
    listOfEmployees = userProfileQuery.filter(~Q(position="client"), company=userCompany, )
    active_registrations = len(listOfEmployees.filter(company__braintree__settings__account__status='active'))

    dateStart = "1900-01-01"
    dateStart = datetime.datetime.strptime(dateStart, "%Y-%m-%d")
        
    if request.method == "POST":
        answer = request.POST
        print(answer)
        if 'facilitySelect' in answer.keys():
            if answer['facilitySelect'] != '':
                return redirect('sup_dashboard', answer['facilitySelect'])
        else:
            if 'facilityInfoSave' in answer.keys():
                form = bat_info_form(answer, instance=facInfoMain)
                if form.is_valid():
                    form.save()
                    #print('saved it')
                    return redirect('selectedFacilitySettings', facility, facilityID, 'main')
            elif 'batteryDashSave' in answer.keys():
                accountData.settings['dashboard'][str(facInfoMain.id)]['batteryDash'] = {}
                batDashSettings = accountData.settings['dashboard'][str(facInfoMain.id)]['batteryDash']
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
                
                A  = accountData
                A.save()
                return redirect('selectedFacilitySettings', facility, facilityID, 'main')
            elif 'notifSettingsForm' in answer.keys():
                accountData.settings['notifications'] = {}
                notificatoinSettingsData = accountData.settings['notifications']
                notifOptions = ['compliance', 'deviations', 'submitted', '10_day_pt', '5_day_pt']
                for notifOp in notifOptions:
                    notificatoinSettingsData[notifOp] = False
                    if notifOp in answer.keys():
                        if answer[notifOp] == 'true':
                            notificatoinSettingsData[notifOp] = True
                            
                A = accountData
                A.save()
                return redirect('selectedFacilitySettings', facility, facilityID, 'main')
            elif 'defaultBatteryDash' in answer.keys():
                if answer['defaultBatteryDash'] == 'true':
                    A  = accountData
                    A.settings['dashBoard'] = json.loads(json.dumps(setDefaultSettings(accountData, request.user.username)['dashboard']))
                    A.save()
                    return redirect('selectedFacilitySettings', facility, facilityID, 'main')
            elif 'defaultNotif' in answer.keys():
                if answer['defaultNotif'] == 'true':
                    A  = accountData
                    A.settings['notifications'] = json.loads(json.dumps(defaultNotifications))
                    A.save()
                    return redirect('selectedFacilitySettings', facility, facilityID, 'main')
            
    return render(request, 'supervisor/settings/selected_facility_settings.html',{
        'notifs': notifs,
        'supervisor': supervisor, 
        "client": client, 
        'unlock': unlock,
        'facility': facility,
        'facilityID': facilityID,
        'facilityIDString': str(facilityID),
        'facilityInfo': facilityInfo,
        'facInfoMain': facInfoMain,
        'clientUserProfs': clientUserProfs,
        'selector': selector,
        'accountData': accountData,
        'listOfEmployees': listOfEmployees,
        'accountData': accountData,
        'active_registrations': active_registrations,
        'userProfileQuery': userProfileQuery,
        'dashDict': json.loads(json.dumps(dashDictOptions))
    })