from django.shortcuts import render # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..models import user_profile_model, company_model, braintreePlans
from ..utils import braintreeGateway
import datetime
from django.contrib.sites.shortcuts import get_current_site # type: ignore
from django.utils.encoding import force_bytes # type: ignore
from django.utils.http import urlsafe_base64_encode # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore

lock = login_required(login_url='Login')

@lock
def billing_view(request, step):
    user = request.user
    gateway = braintreeGateway()
    variables = {}
    allPlans = braintreePlans.objects.all()
    
    if step == 'subscription':
        cPlan = []
        for plan in allPlans:
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
        variables['planList'] = cPlan
        link = "landing/braintree/subscription.html"
    elif step == "registration":
        for iPlans in allPlans:
            print(iPlans)
            if iPlans.id == int(request.POST['planId']):
                selectedPlan = iPlans
        print(request.POST)
        variables['selectedPlan'] = selectedPlan
        link = "landing/braintree/select_registration_amount.html"
    elif step == "payment":
        print(request.POST)
        seats = request.POST['seats']
        addRegistrationCost = format(int(seats)*75, '.2f')
        accountData = user_profile_model.objects.get(user__id=user.id)
        customerId = accountData.company.braintree.settings['account']['customer_ID']
        for plan in allPlans:
            if plan.id == int(request.POST['planId']):
                planDetails = plan
        totalCost = format(float(planDetails.price) + float(addRegistrationCost), '.2f')
        if customerId and customerId != 'none':
            print("check 1")
            customer = gateway.customer.find(customerId)
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
                userCompany.braintree.settings['account']['customer_ID'] = str(newCustomer.customer.id)
                userCompany.braintree.save()
                userCompany.save()
                customer = gateway.customer.find(userCompany.braintree.settings['account']['customer_ID'])
            else:
                for i in newCustomer.errors.deep_errors:
                    print(i.code)
                    if i.code == "81724":
                        print("Duplicate customer exists.")
        cardsOnFile = customer.credit_cards
        print(cardsOnFile)
        cardData = request.POST.get('payNonce', False)
        dataTemplateUse = request.POST
        if 'payNonce' in request.POST.keys():
            cardData = gateway.payment_method_nonce.find(request.POST['payNonce'])
        else:
            cardData = False
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
        link = "landing/braintree/select_payment.html"    
    elif step == "receipt":
        print(request.POST)
        seats = request.POST['seats']
        accountData = user_profile_model.objects.get(user__username=user.username)
        customerId = accountData.company.braintree.settings['account']['customer_ID']
        for plan in allPlans:
            if plan.id == int(request.POST['planId']):
                planDetails = plan
        addRegistrationCost = format(int(seats)*75, '.2f')
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
                "plan_id": planDetails.planID
            })
        else:
            vaultPaymentToken = accountData.company.braintree.settings['payment_methods']['default']['payment_token']
            addOnEdits = {
                "payment_method_token": vaultPaymentToken,
                "plan_id": planDetails.planID
            }
            if int(seats) == 0:
                addOnEdits["add_ons"] = {
                    "remove": ["86gr"]
                }
            else:
                addOnEdits["add_ons"] = {
                    "update": [{
                        "existing_id": "86gr",
                        "quantity": int(seats)
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
            userComp.braintree.settings['payment_methods']['payment_token'] = vaultPaymentToken
            userComp.braintree.settings['subscription']['subscription_ID'] = addSubsriptionResult.subscription.transactions[0].subscription_id
            userComp.braintree.settings['subscription']['plan_id'] = planDetails.planID
            userComp.braintree.settings['subscription']['plan_name'] = planDetails.name
            userComp.braintree.settings['subscription']['price'] = totalCost
            userComp.braintree.settings['subscription']['registrations'] = int(request.POST['seats']) + 2
            userComp.braintree.settings['subscription']['next_billing_date'] = str(datetime.datetime.today().date())
            userComp.braintree.settings['account']['status'] = 'active'
            userComp.braintree.save()
            userComp.save()
            
            mail_subject = 'MethodPlus: Welcome to MethodPlus+. Your account has been activated.'   
            current_site = get_current_site(request)
            html_message = render_to_string('email/acc_welcome_email.html', {  
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            })
            plain_message = strip_tags(html_message)
            to_email = user.email 
            send_mail(
                mail_subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [to_email],
                html_message=html_message,
                fail_silently=False
            )
            print('MADE IT TO FUCKING SAVE')

        variables['totalData']  = request.POST
        variables['planDetails'] = planDetails
        variables['addRegistrationCost'] = addRegistrationCost
        variables['totalCost'] = totalCost
        link = "landing/braintree/landing_select_receipt.html"
        
    return render(request, link, variables)

def landing_addCard_view(request, planId, seats):
    link = 'landing/braintree/landing_addCard.html'
    accountData = user_profile_model.objects.get(user__id=request.user.id)
    gateway = braintreeGateway()
    customerId = accountData.company.braintree.settings['account']['customer_ID']
    variables = {}
    customer = gateway.customer.find(customerId)
    
    print("maide it through the second add")
    print(request.POST)
    if customerId and customerId not in ['none', False]:
        client_token = gateway.client_token.generate({
            "customer_id": customerId
        })
    else:
        client_token = gateway.client_token.generate()
    customer = gateway.customer.find(customerId)
    # customer = gateway.customer.find("the_customer_id")
    # customer.payment_methods # array of braintree.PaymentMethod instances

    variables['customer'] = customer
    variables['client_token'] = client_token
    variables['pId'] = planId
    variables['seats'] = seats
    return render(request, link, variables)