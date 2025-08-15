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
from datetime import datetime, timezone
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


def _ts_to_dt(ts):
    return datetime.fromtimestamp(ts, tz=timezone.utc) if ts else None

def _extra_users_from_subscription(sub):
    EXTRA_USERS_PRICE_IDS = {"price_1RDfPF4SO9L4wW3Id0wHM37O"}  # <-- your "extra users" Price ID(s)
    """Prefer counting the 'extra users' subscription item quantity; fallback to metadata."""
    try:
        items = (sub.get("items") or {}).get("data", []) or []
        for item in items:
            price_id = (item.get("price") or {}).get("id")
            if price_id in EXTRA_USERS_PRICE_IDS:
                return int(item.get("quantity") or 0)
    except Exception:
        pass
    # fallback to subscription metadata, if you ever mirror it there
    return int((sub.get("metadata") or {}).get("extra_users_count", 0))


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature")

    etype = event["type"]
    obj = event["data"]["object"]

    try:
        if etype == "checkout.session.completed":
            # Only logging here; DB work happens on subscription.created/updated
            session = obj
            print("✅ Stripe Checkout completed:",
                  "Session:", session.get("id"),
                  "Subscription:", session.get("subscription"),
                  "Customer:", session.get("customer"))

        elif etype == "customer.subscription.created":
            sub = obj
            subscription_id = sub["id"]
            customer_id = sub.get("customer")
            status = sub.get("status")
            cancel_at_period_end = bool(sub.get("cancel_at_period_end", False))
            next_billing_date = _ts_to_dt(sub.get("current_period_end"))

            # You were expecting these in metadata (only reliable if you add them when creating the sub)
            metadata = sub.get("metadata") or {}
            plan_name = metadata.get("plan", "unknown")
            extra_users = _extra_users_from_subscription(sub)
            user_id = metadata.get("userID")

            if not user_id:
                print("⚠️ No userID in subscription metadata; skipping welcome flow.")
                # Still create/update the subscription record
            user = User.objects.filter(id=user_id).first() if user_id else None
            company = getattr(getattr(user, "user_profile", None), "company", None) if user else None

            # Plan lookup (your model is named braintreePlans)
            plan_obj = None
            try:
                plan_obj = braintreePlans.objects.get(name=plan_name)
            except braintreePlans.DoesNotExist:
                print(f"⚠️ Plan '{plan_name}' not found in braintreePlans.")

            # Create or update local subscription
            sub_defaults = {
                "companyChoice": company,
                "plan": plan_obj,
                "status": status,
                "customerID": customer_id,
                "next_billing_date": next_billing_date,
                "settings": {
                    "extra_users": extra_users,
                    "cancel_at_period_end": cancel_at_period_end,
                },
            }
            sub_obj, created = subscription.objects.update_or_create(
                subscriptionID=subscription_id,
                defaults=sub_defaults,
            )

            # Welcome email only on first create and if we have a user
            if created and user:
                mail_subject = 'MethodPlus: Welcome to MethodPlus+. Your account has been activated.'
                current_site = get_current_site(request)
                html_message = render_to_string('email/acc_welcome_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                })
                plain_message = strip_tags(html_message)
                send_mail(
                    mail_subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False
                )
                print(f"✅ Subscription {subscription_id} created and welcome email sent.")

        elif etype == "customer.subscription.updated":
            sub = obj
            subscription_id = sub["id"]
            status = sub.get("status")
            cancel_at_period_end = bool(sub.get("cancel_at_period_end", False))
            next_billing_date = _ts_to_dt(sub.get("current_period_end"))
            extra_users = _extra_users_from_subscription(sub)

            # Keep schema consistent with 'created' block (plural 'extra_users')
            subscription.objects.filter(subscriptionID=subscription_id).update(
                status=status,
                next_billing_date=next_billing_date,
                settings__extra_users=extra_users,
                settings__cancel_at_period_end=cancel_at_period_end,
            )

        elif etype == "customer.subscription.deleted":
            subID = obj["id"]
            # Also set cancel flag in settings for consistency
            subscription.objects.filter(subscriptionID=subID).update(
                status="canceled",
                settings__cancel_at_period_end=True,
            )

        # (Optional) handle invoice.paid / invoice.payment_failed, etc.

    except Exception as e:
        # Log and return 500 so Stripe retries
        print(f"❌ Webhook error on {etype}: {e}")
        return HttpResponse(status=500)

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