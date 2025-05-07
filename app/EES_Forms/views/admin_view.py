from django.shortcuts import render # type: ignore
import braintree # type: ignore
import os
from ..models import FAQ_model, braintree_model
from ..forms import FAQ_form
from ..utils.main_utils import braintreeGateway, get_list_of_braintree_status

def adminDash(request, selector):
    variables = {
        'selector': selector
    }
    gateway = braintreeGateway()
    btSearchResults = gateway.subscription.search(
        braintree.SubscriptionSearch.status.in_list(
            braintree.Subscription.Status.Active,
            braintree.Subscription.Status.Canceled,
            braintree.Subscription.Status.Expired,
            braintree.Subscription.Status.PastDue,
            braintree.Subscription.Status.Pending
        )
    )

    if selector == "overview":
        active_users, past_due_list = get_list_of_braintree_status(btSearchResults, True)
        
        mmr_total = 0
        for user in active_users:
            user_base_price = int(user['price'])
            user_add_ons_price = 0
            for add_on in user["add_ons"]:
                addOnQuantity = int(add_on['quantity'])
                addOnPrice = int(add_on['amount'])
                addOnTotal = addOnQuantity * addOnPrice
                user_add_ons_price += addOnTotal
            user_monthly_total = user_base_price + user_add_ons_price
            mmr_total += user_monthly_total

        number_of_active_users = len(active_users)
        
        variables['number_of_active_users'] = number_of_active_users
        variables["active_users"] = active_users
        variables['mmr_total'] = mmr_total
        variables['past_due_subscriptions'] = len(past_due_list)
    elif selector == "users":
        print("users")
    elif selector == "subscriptions":
        active_users, past_due_list = get_list_of_braintree_status(btSearchResults, False)
        variables["active_users"] = active_users
    elif selector == "reports":
        active_users, past_due_list = get_list_of_braintree_status(btSearchResults, False)
        variables["active_users"] = active_users
    elif selector == "settings":
        print("settings")

    # Get traffic data for the last 7 days after setting up Google API in CRON.py
    # today = date.today()
    # last_week = today - timedelta(days=7)
    # traffic_data = TrafficData.objects.filter(date__range=(last_week, today))    

    # Output the results
    # print(f"Number of Active Users: {len(active_users)}")
    # for user in active_users:
    #     print(f"Customer ID: {user['customer_id']}")
    #     print(f"Name: {user['first_name']} {user['last_name']}")
    #     print(f"Email: {user['email']}")
    #     print(f"Subscription ID: {user['subscription_id']}")
    #     print(f"Plan ID: {user['plan_id']}")
    #     print(f"Price: {user['price']}")
    #     print(f"Next Billing Date: {user['next_billing_date']}")
    #     print("Add-Ons:")
    #     for add_on in user["add_ons"]:
    #         print(f"  Add-On ID: {add_on['id']}")
    #         print(f"  Name: {add_on['name']}")
    #         print(f"  Amount: {add_on['amount']}")
    #         print(f"  Quantity: {add_on['quantity']}")
    #     print("-----------------------------")


    # customer = gateway.customer.find("226064165")
    # print(customer)
    
    # search_results = gateway.subscription.search(
    #     braintree.SubscriptionSearch.status == braintree.Subscription.Status.Active
    # )
    # for x in search_results:
    #     print(x.id)
        
    # search_results = gateway.subscription.search(
    #     braintree.SubscriptionSearch.status.in_list(
    #         braintree.Subscription.Status.Active,
    #         braintree.Subscription.Status.Canceled,
    #         braintree.Subscription.Status.Expired,
    #         braintree.Subscription.Status.PastDue,
    #         braintree.Subscription.Status.Pending
    #     )
    # )

    #___________VARIABLES________
    # {
    #     #'search_results': search_results,
    #     # 'traffic_data': traffic_data
    # }
    
    return render(request, 'admin/admin_dashboard.html', variables)

def admin_add_FAQ_view(request):
    if request.method == "POST":
        data = request.POST
        form = FAQ_form(data)
        print(form.errors)
        if form.is_valid():
            form.save()
    return render(request, 'admin/admin_add_FAQ.html', {})
    