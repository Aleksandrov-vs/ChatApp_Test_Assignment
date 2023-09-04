import os
from celery.schedules import timedelta

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://127.0.0.1:6379/0")

CELERY_BEAT_SCHEDULE = {
    'create_and_send_report': {
        'task': 'code_monitoring.tasks.create_and_send_report',
        'schedule': timedelta(seconds=5),
    }
}

