from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

os.getenv('DJANGO_SETTINGS_MODULE')

app = Celery('e-commerce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
