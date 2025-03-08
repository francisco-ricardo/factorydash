import factorydash  # This will set up the Django environment

import os
from celery import Celery
from celery.schedules import crontab
from urllib.parse import urlparse

# Default broker and backend URLs (e.g., for local Docker Redis)
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

# Fetch and validate LOAD_NIST_DATA_SCHEDULE_SECONDS (in seconds)
DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS = 60.0  # Default: 60 seconds
LOAD_NIST_DATA_SCHEDULE_SECONDS = os.getenv('LOAD_NIST_DATA_SCHEDULE_SECONDS', str(DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS))
try:
    LOAD_NIST_DATA_SCHEDULE_SECONDS = float(LOAD_NIST_DATA_SCHEDULE_SECONDS)
    if LOAD_NIST_DATA_SCHEDULE_SECONDS <= 0:
        raise ValueError("LOAD_NIST_DATA_SCHEDULE_SECONDS must be a positive number")
except ValueError as e:
    raise ValueError(f"Invalid LOAD_NIST_DATA_SCHEDULE_SECONDS: {e}. Must be a positive number in seconds.")

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Apply additional configuration
app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,  # Retry on connection failure
    broker_connection_max_retries=5,  # Limit retries
    task_track_started=True,  # Track task start time
    result_expires=3600,  # Results expire after 1 hour
)

# Auto-discover tasks from Django apps
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    "load_nist_data_task_every_interval": {
        "task": "monitoring.tasks.load_nist_data_task",
        "schedule": LOAD_NIST_DATA_SCHEDULE_SECONDS,  # Execute every interval (seconds)
    },
    "cleanup_old_data_daily_1": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": crontab(hour=12, minute=5),  # Run daily at 12:05
    },
    "cleanup_old_data_daily_2": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": crontab(hour=0, minute=5),  # Run daily at 00:05
    },
}

# EOF
