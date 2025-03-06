import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')  # Change `lms_backend` to your project name

app = Celery('lms_backend')  # Change to match your project name

app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed apps
app.autodiscover_tasks()
