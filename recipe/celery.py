from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import django

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

# Initialize Django
django.setup()

app = Celery('recipe')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in all registered Django apps
app.autodiscover_tasks()

# Optional: Define a simple task to test if Celery is working
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
