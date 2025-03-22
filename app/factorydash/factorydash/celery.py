import os
from celery import Celery
from celery.schedules import crontab
from urllib.parse import urlparse

# Default broker and backend URLs
DEFAULT_CELERY_BROKER_URL = 'redis://redis:6379/0'
DEFAULT_CELERY_RESULT_BACKEND = DEFAULT_CELERY_BROKER_URL

# Fetch and validate broker URLs
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', DEFAULT_CELERY_BROKER_URL)
if not CELERY_BROKER_URL:
    raise ValueError("CELERY_BROKER_URL must be set to a valid broker URL")
try:
    parsed_url = urlparse(CELERY_BROKER_URL)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("CELERY_BROKER_URL must be a valid URL (e.g., redis://host:port)")
except ValueError as e:
    raise ValueError(f"Invalid CELERY_BROKER_URL: {e}")
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', DEFAULT_CELERY_RESULT_BACKEND)

# Fetch and validate LOAD_NIST_DATA_SCHEDULE_SECONDS
DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS = 60.0
LOAD_NIST_DATA_SCHEDULE_SECONDS = os.getenv('LOAD_NIST_DATA_SCHEDULE_SECONDS', str(DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS))
try:
    LOAD_NIST_DATA_SCHEDULE_SECONDS = float(LOAD_NIST_DATA_SCHEDULE_SECONDS)
    if LOAD_NIST_DATA_SCHEDULE_SECONDS <= 0:
        raise ValueError("LOAD_NIST_DATA_SCHEDULE_SECONDS must be a positive number")
except ValueError as e:
    raise ValueError(f"Invalid LOAD_NIST_DATA_SCHEDULE_SECONDS: {e}")

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
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
        "schedule": LOAD_NIST_DATA_SCHEDULE_SECONDS,
    },
    "cleanup_old_data_daily_midday": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": crontab(hour=12, minute=5),
    },
    "cleanup_old_data_daily_midnight": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": crontab(hour=0, minute=5),
    },
    "update_dashboard_every_interval": {
        "task": "monitoring.tasks.update_dashboard",
        "schedule": 5,
    },
}

# EOF
