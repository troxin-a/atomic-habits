import requests
from celery import shared_task

from config.settings import TELEGRAM_API_TOKEN, TELEGRAM_API_URL


@shared_task
def send_message(chat_id, text):
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(url=f"{TELEGRAM_API_URL}bot{TELEGRAM_API_TOKEN}/sendmessage", data=data)
