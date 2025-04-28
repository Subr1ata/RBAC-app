import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('marketing_app')
app.conf.from_object("django.conf:settings", namespace="CELERY")

@app.task
def add_numbers(x, y):
    return x + y

app.autodiscover_tasks()
