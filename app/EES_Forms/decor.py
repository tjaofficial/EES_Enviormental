import braintree
from django.shortcuts import redirect
from .utils import braintreeGateway
from .models import user_profile_model

# def client_redirect(x):
#     if not x.groups.filter(name='SGI Technician') or x.is_superuser:
#         return redirect('c_dashboard')
     
# client = client_redirect

def isSubActive(func):
    def wrapper(request, facility, *args, **kwargs):
        gateway = braintreeGateway()
        accountData = user_profile_model.objects.get(user__username=request.user.username)
        print(accountData.company.customerID)
        customerId = accountData.company.customerID
        if not customerId or customerId == 'none':
            status = False
            print("no customer ID")
        else:
            status = True
            print(gateway.customer.find(customerId))
        #V------get rid of the status=True for prod-----V
        status = True    
        if status:
            return func(request, facility, *args, **kwargs)
        else:
            return redirect('subscriptionSelect', facility, 'subscription')
    return wrapper