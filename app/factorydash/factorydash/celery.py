import factorydash  # This will set up the Django environment

from celery import Celery
from celery.schedules import crontab

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from Django apps
app.autodiscover_tasks()

# Tasks scheduling (Celery Beat)
app.conf.beat_schedule = {
    "load_nist_data_task_every_10_seconds": {
        "task": "monitoring.tasks.load_nist_data_task",
        "schedule": 10.0,  # Execute every 10 seconds
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
