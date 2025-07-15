from django.shortcuts import render # type: ignore
import braintree # type: ignore
from django.contrib.auth.decorators import login_required, user_passes_test  # type: ignore
from django.contrib.auth.models import User # type: ignore
from ..models import FAQ_model
from django.http import JsonResponse # type: ignore
from ..forms import FAQ_form
from django.shortcuts import get_object_or_404, redirect # type: ignore
from django.contrib.auth import login, get_user_model  # type: ignore
from ..utils.main_utils import braintreeGateway, get_list_of_braintree_status

@login_required
@user_passes_test(lambda u: u.is_staff)
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
        
    return render(request, 'admin/admin_dashboard.html', variables)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_add_FAQ_view(request):
    if request.method == "POST":
        data = request.POST
        form = FAQ_form(data)
        print(form.errors)
        if form.is_valid():
            form.save()
    return render(request, 'admin/admin_add_FAQ.html', {})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user_companies(request):
    if request.method == "POST":
        data = request.POST
        form = FAQ_form(data)
        print(form.errors)
        if form.is_valid():
            form.save()
    return render(request, 'admin/admin_add_FAQ.html', {})

@login_required
@user_passes_test(lambda u: u.is_staff)  # adjust as needed
def get_users_json(request):
    users = User.objects.select_related("user_profile__company").all()

    data = []
    for user in users:
        if not getattr(user, "user_profile", False):
            continue
        company = getattr(user.user_profile.company, 'company_name', 'N/A') if hasattr(user, 'user_profile') else 'N/A'
        position = getattr(user.user_profile, 'position', 'N/A')
        status = "Active" if user.is_active else "Inactive"
        number = user.user_profile.phone

        data.append({
            "name": f"{user.first_name} {user.last_name}".strip(),
            "company": company,
            "position": position,
            "number": number,
            "email": user.email,
            "settings": "Edit",  # You can make this a link if needed
            "status": status,
            "userID": user.id
        })

    return JsonResponse({"users": data})    

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def login_as_user(request, user_id):
    User = get_user_model()
    target_user = get_object_or_404(User, id=user_id)
    
    # Optional: prevent impersonating other superusers
    if target_user.is_superuser:
        return redirect("forbidden")  # or raise 403
    

    original_user_id = request.session.get("original_user_id", request.user.id)
    impersonating = True

    login(request, target_user)

    request.session["original_user_id"] = original_user_id
    request.session["impersonating"] = impersonating

    return redirect("sup_dashboard")

@login_required
def return_to_admin(request):
    admin_id = request.session.get("original_user_id")
    if admin_id:
        admin_user = get_user_model().objects.get(id=admin_id)
        login(request, admin_user)
        request.session.pop("original_user_id", None)
        request.session.pop("impersonating", None)
        return redirect("adminDash", "users")  # your real admin area
    return redirect("Login")