from django.http import JsonResponse # type: ignore
from datetime import datetime, timezone
import stripe # type: ignore
import braintree # type: ignore
from django.conf import settings # type: ignore
from ..utils.main_utils import braintreeGateway
from ..models import braintreePlans

stripe.api_key = settings.STRIPE_SECRET_KEY
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
    # try:
    # Get all subscriptions (paginated)
    subscriptions = stripe.Subscription.list(limit=100)

    active_count = 0
    past_due_count = 0
    monthly_revenue = 0
    subscriptions_data = []

    for sub in subscriptions.auto_paging_iter():
        print(sub)
        subscriptions_totals = 0
        status = sub.status
        customer_id = sub.customer
        items = sub.get("items")
        for item in items['data']:
            cost = item['plan']['amount']/ 100.0
            quantity = item['quantity']
            sub_total = cost * quantity
            subscriptions_totals += sub_total 
        created = sub.get("created")
        next_billing = sub.get("current_period_end")

        # Get customer details
        customer = stripe.Customer.retrieve(customer_id)
        name = customer.name or customer.email or "Unknown"

        if status == "active":
            active_count += 1
        elif status == "past_due":
            past_due_count += 1

        created_dt = datetime.fromtimestamp(created, tz=timezone.utc) if created else None
        next_billing_dt = datetime.fromtimestamp(next_billing, tz=timezone.utc) if next_billing else None

        # Get current month's revenue (rough estimation)
        current_month = datetime.now(timezone.utc).replace(day=1)
        if created_dt and created_dt >= current_month.replace(tzinfo=timezone.utc):
            monthly_revenue += subscriptions_totals

        # Formatted strings
        start_date = created_dt.strftime("%Y-%m-%d") if created_dt else "N/A"
        next_billing_date = next_billing_dt.strftime("%Y-%m-%d") if next_billing_dt else "N/A"

        subscriptions_data.append({
            "id": sub.id,
            "customer_name": name,
            "status": status.capitalize(),
            "start_date": start_date,
            "next_billing_date": next_billing_date,
        })

    return JsonResponse({
        "subscriptions": subscriptions_data,
        "active_users": active_count,
        "past_due": past_due_count,
        "monthly_revenue": f"${monthly_revenue:.2f}"
    })

    # except Exception as e:
    #     return JsonResponse({"error": str(e)}, status=500)