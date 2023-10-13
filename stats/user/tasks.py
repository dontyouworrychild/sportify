from core.celery import APP

from .utils import send_sms


@APP.task()
def send_phone_notification(user_data):
    send_sms(user_data['phone_number'], user_data['message'])