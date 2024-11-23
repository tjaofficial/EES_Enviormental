import datetime
import logging
from django.db.models.functions import Cast
from .models import braintree_model,user_profile_model
from .utils import getActiveCompanyEmployees
from django.db.models import DateField
from django.db.models import Q # type: ignore

# Configure logging
logging.basicConfig(
    filename="/tmp/cron_job.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def check_subscription_expiry():
    print('HOLY SHIT CRON RAN')
    logging.info("Cron job started")
    today = datetime.datetime.today().date()
    braintreeQuery = braintree_model.objects.all()
    for subscription in braintreeQuery:
        subSettings = subscription.settings['subscription']
        if subSettings:
            if datetime.datetime.strptime(subSettings['next_billing_date'],"%Y-%m-%d").date() <= today:
                mainSupervisorProf = user_profile_model.objects.get(user=subscription.user)
                listOfEmployees = getActiveCompanyEmployees(mainSupervisorProf.company)
                print(listOfEmployees)
                for emp in listOfEmployees:
                    if emp == mainSupervisorProf:
                        continue
                    else:
                        user = emp.user
                        user.is_active = False
                        user.save()
                        userProf = emp
                        userProf.settings['position'] = userProf.settings['position'] + "-activate"
                        userProf.save()
                        logging.info(f"Deactivated user: {user.username}")

def check_subscription_activations():
    