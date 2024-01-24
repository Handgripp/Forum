from celery import Celery, shared_task
from django.core.mail import send_mail
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum.settings')

celery_app = Celery('forum')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')


@shared_task()
def send_async_email(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)



