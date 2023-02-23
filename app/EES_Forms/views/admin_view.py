from django.shortcuts import render
import braintree
import os

def adminDash(request):
    print('hello')
    # gateway = braintree.BraintreeGateway(
    #     braintree.Configuration(
    #         braintree.Environment.Sandbox,
    #         merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
    #         public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
    #         private_key=os.environ.get('BRAINTREE_PRIVATE_KEY')
    #     )
    # )
    # customer = gateway.customer.find("a_customer_id")
    # print(customer)
    
    
    return render(request, 'admin/admin_dashboard.html', {
        
    })
    