import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'converter.settings')

app = Celery('converter')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_currency': {
        'task': 'update_currency',
        'schedule': crontab(minute='*/30', hour='0,12')  # Every 30 minutes, at 12:00 AM and 12:00 PM Europe/Moscow
    },
}
