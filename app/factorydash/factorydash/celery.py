"""
This module configures and initializes Celery for the factorydash project.

It sets up the Celery application, configures the broker and result backend,
defines task serialization and other settings, and establishes the Celery Beat
schedule for periodic tasks.

The module also handles the auto-discovery of tasks from the project's apps.
"""
from celery import Celery
from celery.schedules import timedelta
from django.conf import settings

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=5,
    task_track_started=True,
    result_expires=3600,
)

# Auto-discover tasks
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    "load_nist_data_task_every_interval": {
        "task": "monitoring.tasks.load_nist_data_task",
        "schedule": settings.LOAD_NIST_DATA_SCHEDULE_SECONDS,
    },
    "cleanup_old_data_every_interval": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": timedelta(hours=settings.CLEANUP_OLD_DATA_SCHEDULE_HOURS),
    },
    "update_dashboard_every_interval": {
        "task": "monitoring.tasks.update_dashboard",
        "schedule": settings.UPDATE_DASHBOARD_SCHEDULE_SECONDS,
    },
}

# EOF
