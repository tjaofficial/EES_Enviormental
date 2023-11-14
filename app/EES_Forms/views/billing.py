
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import user_profile_model, company_model
import braintree
import os

lock = login_required(login_url='Login')

@lock
def billing(request, step):
    user = request.user
    userProfile = user_profile_model.objects.filter(user__username=request.user.username)
    print(userProfile)
    if len(userProfile)>0: 
        userProfile = userProfile[0]
    #need to get customer id when one is present
    #MOCK DB VALUES
    customerId = None
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
            public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
            private_key=os.environ.get('BRAINTREE_PRIVATE_KEY')
        )
    )

    if step == "subscriptions":
        plans = gateway.plan.all()
        cPlan = []

        for plan in plans:
            oPlan = {
                'pid': plan.id,
                'billingDOM': plan.billing_day_of_month,
                'currency_iso_code': plan.currency_iso_code,
                'description': plan.description.split("\n"),
                'name': plan.name,
                'price': plan.price
                }
            cPlan.append(oPlan)
        cPlan.sort(key=lambda d: d['price'])
        template = "admin/billing/subscription.html"
        pVars = {'plans':cPlan}

    if step == "customer":
        if request.method == 'POST':
            pId = request.POST['planId']
        else:
            pass
            #return redirect('billing', step = "subscriptions")

        if customerId is None:
            client_token = gateway.client_token.generate()
        else:
            client_token = gateway.client_token.generate({
                "customer_id": customerId
            })
        
        template = "admin/billing/customer.html"
        pVars = {
            'client_token': client_token,
            'pId':pId
        }

    if step == "review":
        template = "admin/billing/review.html"
        pVars = {}

    if step == "receipt":
        if request.method != 'POST':
            pass
            #return redirect('billing', step = "subscriptions")

        else:
            pass
            #return redirect('billing', step = "subscriptions")
        print('Name On Card')
        print(request.POST)
        planId = request.POST['planId']
        print(planId)        
        nameOnCard = request.POST['nameOnCard']
        addressLine1 = request.POST['address1']
        addressLine2 = request.POST['address2']

        city = request.POST['city']
        state = request.POST['state']
        zipCode = request.POST['zipCode']
        nonce_from_the_client = request.POST['payNonce']
        userEmail = user.email
        userFirstName = user.first_name
        userLastName = user.last_name
        userPhone = userProfile.phone
        
        createCustomerResult = gateway.customer.create({
            'company': userProfile.company.company_name,    # str - Company name. Maximum 255 characters.
            'credit_card':{ # A credit or debit payment method.
                'billing_address': { # A billing address associated with a specific credit card. The maximum number of addresses per customer is 50. - 
                    'company': userProfile.company.company_name,   # str - Company name. Maximum 255 characters.
                    'country_code_alpha2': 'US',    # str - The ISO 3166-1 alpha-2 country code specified in an address. The gateway only accepts specific alpha-2 values.
                    'extended_address': addressLine2,   # str - The extended address information—such as apartment or suite number. 255 character maximum.
                    #'first_name': ,    # str - The first name. Maximum 255 characters.
                    #'last_name': ,    # str - The last name. Maximum 255 characters.
                    'locality': city,    # str - The locality/city. Maximum 255 characters.
                    'postal_code': zipCode,    # str - The postal code. Postal code must be a string of 4-9 alphanumeric characters, optionally separated by a dash or a space. Spaces and hyphens are ignored.
                    'region': state,    # str - The state or province. Maximum 255 characters.
                    'street_address': addressLine1,   # str - The street address. Maximum 255 characters.  
                },    
                'cardholder_name': nameOnCard,    # str - The name associated with the credit card. Must be less than or equal to 175 characters.
                'options':{ # Optional values that can be passed with a request. - 
                    'fail_on_duplicate_payment_method': True,    # bool - If this option is passed and the same payment method has already been added to the Vault for any customer, the request will fail. This option will be ignored for PayPal, Pay with Venmo, Apple Pay, Google Pay, and Samsung Pay payment methods.
                    'make_default': True,    # bool - This option makes the specified payment method the default for the customer.
                    'skip_advanced_fraud_checking': False,    # boolean - If the payment method is a credit card, prevents the verification from being evaluated as part of Premium Fraud Management Tools checks. Use with caution – once you've skipped checks for a verification, it is not possible to run them retroactively.:     #  - 
                    'verify_card': True,   # bool - If the payment method is a credit card, this option prompts the gateway to verify the card's number and expiration date. It also verifies the AVS and CVV information if you've enabled AVS and CVV rules.:     #  - NOTE Braintree strongly recommends verifying all cards before they are stored in your Vault by enabling card verification for your entire account in the Control Panel. In some cases, cardholders may see a temporary authorization on their account after their card has been verified. The authorization will fall off the cardholder's account within a few days and will never settle.:     #  - Only returns a CreditCardVerification result if verification runs and is unsuccessful.
                }     
                #'token':     # str - An alphanumeric value that references a specific payment method stored in your Vault. Must be less than or equal to 36 characters. If using a custom integration, you can specify what you want the token to be. If not specified, the gateway will generate one that can be accessed on the result. If using our Drop-in UI with a customer ID to vault payment methods, you can't specify your own token. Length and format of gateway-generated tokens and IDs may change at any time.:     #  - 
            } ,
            'email': userEmail,    # str - Email address composed of ASCII characters.
            'first_name':userFirstName ,    # str - The first name. The first name value must be less than or equal to 255 characters.
            #'id': ,    # str - A string value that will represent this specific customer in your Vault. 36 character maximum; must be unique within your Vault; valid characters are letters, numbers, -, and _; the words "all" and "new" currently can't be used. If not specified on creation, the gateway will generate an alphanumeric ID that can be accessed on the result. The generated IDs will never start with a leading 0 and are case insensitive.:     #  - 
            'last_name': userLastName,    # str - The last name. The last name value must be less than or equal to 255 characters.
            'payment_method_nonce':  nonce_from_the_client,   # str - One-time-use reference to payment information provided by your customer, such as a credit card or PayPal account. When passed on customer create, it creates a payment method associated with the new customer; see example below.
            'phone': userPhone,    # str - Phone number. Maximum 255 characters.
        })

        if not createCustomerResult.is_success:
            print(createCustomerResult)
            for i in createCustomerResult.errors.deep_errors:
                print(i.code)
                #---------------------------------------
                #---------------------------------------
                # Need to setup somthing to catch the error codes
                # given from Braintree. If there is an error the
                # submission wont process (obviously) and wont
                # create the next variable reliant on success.
                #---------------------------------------
                #---------------------------------------
                if i.code == "81724":
                    print("Duplicate card exists.")
            #print("ERROR: Issue with creating costumer")
        
        vaultCustomerId = createCustomerResult.customer.id
            
        userComp = company_model.objects.filter(company_name=userProfile.company.company_name)
        if len(userComp) > 0:
            userComp = userComp[0]
        else:
            print("No Compnay has been entered for user profile information")
        userComp.customerID = vaultCustomerId
        userComp.save()

        #store the customer ID to th client that it is assocatited with

        vaultPaymentToken = createCustomerResult.customer.payment_methods[0].token
        addSubsriptionResult = gateway.subscription.create({
            "payment_method_token": vaultPaymentToken,
            "plan_id": planId
        })

        if not addSubsriptionResult.is_success:
            for i in addSubsriptionResult.errors.deep_errors:
                print(i)
        else:
            userComp.payment_method_token = vaultPaymentToken
            userComp.save()
        
        # for x in addSubsriptionResult:
        #     print(x)
        #     break
        #on success and active 


        template = "admin/billing/receipt.html"
        pVars = {'information':"Congrats the sub was created"}



    # pass client_token to your front-end

    # if client_token.errors.size != 0:
    #     for error in client_token.errors.deep_errors:
    #         print(error.code)
    #         print(error.message)
    #     return HttpResponseServerError
    
    return render(request,template,pVars)








# result.subscription_id