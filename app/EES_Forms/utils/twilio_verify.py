from twilio.rest import Client # type: ignore
from django.conf import settings # type: ignore
from twilio.base.exceptions import TwilioRestException # type: ignore

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_verification_code(phone_number):
    try:
        verification = client.verify.v2.services(
            settings.TWILIO_VERIFY_SERVICE_SID
        ).verifications.create(
            to=phone_number,
            channel='sms'
        )
        return verification.status
    except TwilioRestException as e:
        if e.status == 429:
            return "too_many_attempts"
        raise

def check_verification_code(phone_number, code):
    verification_check = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID).verification_checks.create(
        to=phone_number,
        code=code
    )
    return verification_check.status == "approved"

def send_sms_message(to_number, body):
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_number
    )
    return message.sid