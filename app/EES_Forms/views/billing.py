import stripe # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse # type: ignore
from ..models import braintreePlans, subscription
from EES_Enviormental.settings import CLIENT_VAR, OBSER_VAR, SUPER_VAR
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.contrib.sites.shortcuts import get_current_site # type: ignore
from django.utils.encoding import force_bytes # type: ignore
from django.utils.http import urlsafe_base64_encode # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from ..decor import group_required
from ..models import User
from datetime import datetime
from django.urls import reverse # type: ignore

lock = login_required(login_url='Login')
stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET

def stripe_subscription_view(request):
    plansQuery = braintreePlans.objects.all()

    if request.method == "POST":
        plan = request.POST.get("plan")
        addons = request.POST.getlist("addons")
        extra_users_count = int(request.POST.get("extra_users_count", 0))

        # Match plan/add-ons to Stripe Price IDs
        price_map = {
            **{f"{sub.name}": f"{sub.priceID}" for sub in plansQuery},
            "extra_users": "price_1RQbqCG3aFwevvRDkG83BVZ8"
        }
        print(price_map)

        if plan not in price_map:
            return HttpResponseBadRequest("Invalid plan selected")

        line_items = [
            {"price": price_map[plan], "quantity": 1},
        ]

        if "extra_users" in addons and extra_users_count > 0:
            line_items.append({"price": price_map["extra_users"], "quantity": extra_users_count})

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="subscription",
                line_items=line_items,
                success_url=request.build_absolute_uri("/billing/success/"),
                cancel_url=request.build_absolute_uri("/billing/cancel/"),
                customer_email=request.user.email if request.user.is_authenticated else None,
                metadata={
                    "plan": plan,
                    "extra_users_count": str(extra_users_count),
                    "userID": str(request.user.id)  # optional
                }
            )
            return redirect(session.url)

        except Exception as e:
            return JsonResponse({f"error duh": str(e)}, status=400)

    return render(request, "admin/stripe/subscribe.html", {
        'plansQuery': plansQuery.order_by('price'),
        'jsPlansQuery': list(plansQuery.values('name', 'price', 'description'))
    })

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)  # invalid payload
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)  # invalid signature

    # 🔥 Handle subscription
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        print("✅ Stripe Checkout completed:")
        print("Session ID:", session.get("id"))
        print("Subscription ID:", session.get("subscription"))
        print("Customer ID:", session.get("customer"))
    elif event["type"] == "customer.subscription.deleted":
        subID = event["data"]["object"]["id"]
        subscription_obj = subscription.objects.get(subscriptionID=subID)
        subscription_obj.status = "canceled"
        subscription_obj.save()
    elif event["type"] == "customer.subscription.updated":
        subscription_data = event["data"]["object"]
        subscription_id = subscription_data["id"]
        status = subscription_data["status"]
        cancel_at_period_end = subscription_data.get("cancel_at_period_end", False)
        current_period_end = subscription_data.get("current_period_end")

        #metadata = subscription_data.get("metadata", {})
        extra_users = session["metadata"].get("extra_users_count", "0")
        subscription.objects.filter(subscriptionID=subscription_id).update(
            status=status,
            settings__extra_user=extra_users,
            next_billing_date=datetime.fromtimestamp(current_period_end),
            settings__cancel_at_period_end=cancel_at_period_end
        )
    elif event["type"] == "customer.subscription.created":
        subscription_data = event["data"]["object"]

        subscription_id = subscription_data["id"]
        customer_id = subscription_data["customer"]
        status = subscription_data["status"]
        cancel_at_period_end = subscription_data.get("cancel_at_period_end", False)
        current_period_end = subscription_data.get("current_period_end")

        metadata = subscription_data.get("metadata", {})
        plan = metadata.get("plan", "unknown")
        extra_users = metadata.get("extra_users_count", "0")
        user_id = metadata.get("userID")

        # Safety checks
        if not user_id:
            print("⚠️ No userID found in metadata!")
            return HttpResponse(status=200)

        user = User.objects.filter(id=user_id).first()
        if not user:
            print(f"⚠️ User with ID {user_id} not found!")
            return HttpResponse(status=200)

        company = user.user_profile.company

        try:
            planSelection = braintreePlans.objects.get(name=plan)
        except braintreePlans.DoesNotExist:
            print(f"⚠️ Plan {plan} not found in braintreePlans!")
            return HttpResponse(status=200)

        # Create subscription in your DB
        subscription.objects.create(
            companyChoice=company,
            subscriptionID=subscription_id,
            plan=planSelection,
            status=status,
            customerID=customer_id,
            settings={
                "extra_users": extra_users,
                "next_billing_date": str(datetime.fromtimestamp(current_period_end)),
                "cancel_at_period_end": cancel_at_period_end
            }
        )

        # Send Welcome Email
        mail_subject = 'MethodPlus: Welcome to MethodPlus+. Your account has been activated.'   
        current_site = get_current_site(request)
        html_message = render_to_string('email/acc_welcome_email.html', {  
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
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

        print(f"✅ Subscription {subscription_id} created and welcome email sent.")
            
    # elif event["type"] == "invoice.payment_succeeded":
    #     invoice = event["data"]["object"]
    #     subscription_id = invoice.get("subscription")

    #     print("🔥 invoice.payment_succeeded")
    #     print("  invoice ID:", invoice.get("id"))
    #     print("  subscription ID:", subscription_id)

    #     if not subscription_id:
    #         print("⚠️ Skipping invoice without subscription ID.")
    #         return HttpResponse(status=200)

    #     stripe_subscription = stripe.Subscription.retrieve(subscription_id)
    #     current_period_end = stripe_subscription.get("current_period_end")
    #     print("  Stripe status:", stripe_subscription.get("status"))
    #     print("  current_period_end:", current_period_end)

    #     if current_period_end:
    #         billing_date = datetime.fromtimestamp(current_period_end)
    #         subscription.objects.filter(subscriptionID=subscription_id).update(
    #             settings__next_billing_date=str(billing_date)
    #         )
    #         print("✅ Updated next_billing_date to:", billing_date)
    #     else:
    #         print("⚠️ Stripe subscription has no current_period_end yet.")
    # elif event["type"] == "customer.subscription.created":
    #     subscription_obj = event["data"]["object"]
    #     subscription_id = subscription_obj.get("id")
    #     current_period_end = subscription_obj.get("current_period_end")

    #     print("🔥 customer.subscription.created")
    #     print("  Subscription ID:", subscription_id)
    #     print("  current_period_end:", current_period_end)

    #     if current_period_end:
    #         billing_date = datetime.fromtimestamp(current_period_end)
    #         subscription.objects.filter(subscriptionID=subscription_id).update(
    #             settings__next_billing_date=str(billing_date)
    #         )
    #         print("✅ Updated next_billing_date from subscription.created:", billing_date)
    #     else:
    #         print("⚠️ Subscription still has no billing date in subscription.created.")
    # elif event["type"] == "invoice.finalized":
    #     invoice = event["data"]["object"]
    #     subscription_id = invoice.get("subscription")

    #     print("🔥 invoice.finalized")
    #     print("  invoice ID:", invoice.get("id"))
    #     print("  subscription ID:", subscription_id)

    #     if subscription_id:
    #         stripe_subscription = stripe.Subscription.retrieve(subscription_id)
    #         current_period_end = stripe_subscription.get("current_period_end")

    #         if current_period_end:
    #             billing_date = datetime.fromtimestamp(current_period_end)
    #             subscription.objects.filter(subscriptionID=subscription_id).update(
    #                 settings__next_billing_date=str(billing_date)
    #             )
    #             print("✅ Updated next_billing_date from invoice.finalized:", billing_date)
    #         else:
    #             print("⚠️ Still no current_period_end in finalized invoice.")


    return HttpResponse(status=200)

@lock
@group_required(SUPER_VAR)
def stripe_customer_portal(request):
    try:
        return_url = request.GET.get("next", reverse("Account"))
        subscriptionQuery = request.user.user_profile.company.subscription
        session = stripe.billing_portal.Session.create(
            customer=subscriptionQuery.customerID,
            return_url=request.build_absolute_uri(return_url)
        )
        return redirect(session.url)
    except subscription.DoesNotExist:
        return redirect(return_url)

@lock
def stripe_success(request):
    subscriptionDetails = request.user.user_profile.company.subscription

    registration_cost = 75 * int(subscriptionDetails.settings['extra_users'])
    totalCost = float(subscriptionDetails.plan.price) + registration_cost

    return render(request, "admin/stripe/stripe_success.html",{
        'planDetails': subscriptionDetails,
        'registration_cost': registration_cost,
        'totalCost': totalCost
    })