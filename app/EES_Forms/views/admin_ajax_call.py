from django.http import JsonResponse # type: ignore
import datetime
import braintree # type: ignore
import os
from ..utils.main_utils import braintreeGateway
from ..models import braintreePlans

# Configure Braintree gateway
gateway = braintreeGateway()

def get_monthly_revenue(request):

    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))

    # Define the date range for the specific month
    start_date = datetime.datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime.datetime(year + 1, 1, 1).date()
    else:
        end_date = datetime.datetime(year, month + 1, 1).date()
    # Search for transactions within the date range
    transactions = gateway.transaction.search(
        braintree.TransactionSearch.settled_at.between(start_date, end_date)
    )
    # Calculate total revenue
    total_revenue = sum(float(transaction.amount) for transaction in transactions.items)

    return JsonResponse({"revenue": total_revenue})

def get_subscriptions(request):
    plansQuery = braintreePlans.objects.all()
    btSearchResults = gateway.subscription.search(
        braintree.SubscriptionSearch.status.in_list(
            braintree.Subscription.Status.Active,
            braintree.Subscription.Status.Canceled,
            braintree.Subscription.Status.PastDue,
        )
    )

    subscriptions_data = []

    for sub in btSearchResults.items:
        parsePlan = plansQuery.get(planID=sub.plan_id).name
        transaction = sub.transactions  # Take the first transaction
        if len(transaction) > 0:
            customer = transaction[0].customer_details
        else:
            customer = False
        if customer:
            subscriptions_data.append({
                "id": sub.id,
                "customer_name": f"{customer.first_name} {customer.last_name}",
                "status": sub.status,
                "plan_id": parsePlan,
                "start_date": str(sub.created_at),
                "next_billing_date": str(sub.next_billing_date),
            })

    return JsonResponse({"subscriptions": subscriptions_data})