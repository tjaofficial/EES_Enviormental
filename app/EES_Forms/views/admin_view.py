from django.shortcuts import render
import braintree
import os
from ..models import FAQ_model
from ..forms import FAQ_form

def adminDash(request):
    print('hello')
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
            public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
            private_key=os.environ.get('BRAINTREE_PRIVATE_KEY')
        )
    )
    # customer = gateway.customer.find("226064165")
    # print(customer)
    
    search_results = gateway.subscription.search(
        braintree.SubscriptionSearch.status == braintree.Subscription.Status.Active
    )
    for x in search_results:
        print(x.id)
        
    # search_results = gateway.subscription.search(
    #     braintree.SubscriptionSearch.status.in_list(
    #         braintree.Subscription.Status.Active,
    #         braintree.Subscription.Status.Canceled,
    #         braintree.Subscription.Status.Expired,
    #         braintree.Subscription.Status.PastDue,
    #         braintree.Subscription.Status.Pending
    #     )
    # )
    
    return render(request, 'admin/admin_dashboard.html', {
        'search_results': search_results
    })
    
def admin_add_FAQ_view(request):
    if request.method == "POST":
        data = request.POST
        form = FAQ_form(data)
        print(form.errors)
        if form.is_valid():
            form.save()
    return render(request, 'admin/admin_add_FAQ.html', {})
    