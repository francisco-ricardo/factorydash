from celery import Celery
from celery.schedules import crontab

from factorydash.defaults import default_path_definition

# Set default Django settings
default_path_definition()

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from Django apps
app.autodiscover_tasks()

# Tasks scheduling (Celery Beat)
# TODO: AJUSTAR O SCHEDULE PARA 10 SEGUNDOS
app.conf.beat_schedule = {
    "fetch-nist-data-every-10-seconds": {
        "task": "monitoring.tasks.fetch_nist_data_task",
        "schedule": 600.0,  # Execute every 10 seconds
    },
    "cleanup-old-data-daily": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": crontab(hour=19, minute=15),  # Run daily at 00:00
    },
}



# EOF
