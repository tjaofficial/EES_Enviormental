import datetime
import logging
# from googleapiclient.discovery import build
# from .models import TrafficData
from .models import braintree_model,user_profile_model, account_reactivation_model
from .utils import getActiveCompanyEmployees, braintreeGateway

# Configure logging
logging.basicConfig(
    filename="/tmp/cron_job.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def check_subscription_expiry():
    logging.info("Subscripton Cancel job started")
    today = datetime.datetime.today().date()
    braintreeQuery = braintree_model.objects.all()
    gateway = braintreeGateway()
    for subscription in braintreeQuery:
        subSettings = subscription.settings['subscription']
        if subSettings:
            subID = subSettings['subscription_ID']
            sub = gateway.subscription.find(subID)
            subStatus = sub.status
            if subStatus == "Canceled" and datetime.datetime.strptime(subSettings['next_billing_date'],"%Y-%m-%d").date() < today:
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
            elif sub.status == "Past Due":
                # maybe create an admin log for keeping track of this
                print("Check admin logs for past due accounts")

def check_subscription_activations():
    logging.info("Subscripton Activate job started")
    today = datetime.datetime.today().date()
    activationUsers = account_reactivation_model.objects.all()
    for user in activationUsers:
        if user.reactivation_date <= today:
            userUser = user.user
            userUser.is_active = True
            userUser.save()

            user.delete()

def update_next_billing():
    btQuery = braintree_model.objects.all()
    for btEntry in btQuery:
        if btEntry.settings['subscription']:
            subId = btEntry.settings['subscription']['subscription_ID']
            gateway = braintreeGateway()
            sub = gateway.subscription.find(subId)
            if sub.status == "Active":
                if datetime.datetime.strptime(btEntry.settings['subscription']['next_billing_date'],"%Y-%m-%d").date() < sub.next_billing_date:
                    btEntry.settings['subscription']['next_billing_date'] = str(sub.next_billing_date)
                    btEntry.save()

# def fetch_google_analytics_data():
#     analytics = build('analyticsreporting', 'v4', credentials=YOUR_CREDENTIALS)

#     response = analytics.reports().batchGet(
#         body={
#             'reportRequests': [
#                 {
#                     'viewId': 'YOUR_VIEW_ID',
#                     'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
#                     'metrics': [{'expression': 'ga:pageviews'}, {'expression': 'ga:users'}]
#                 }
#             ]
#         }
#     ).execute()

#     rows = response['reports'][0]['data']['rows']
#     for row in rows:
#         date_str = row['dimensions'][0]
#         pageviews = row['metrics'][0]['values'][0]
#         users = row['metrics'][0]['values'][1]
#         TrafficData.objects.update_or_create(
#             date=date_str,
#             defaults={'views': pageviews, 'unique_visitors': users}
#         )