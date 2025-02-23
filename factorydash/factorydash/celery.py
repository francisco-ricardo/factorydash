import os
from celery import Celery


# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorydash.settings")

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from Django apps
app.autodiscover_tasks()

# Tasks scheduling (Celery Beat)
app.conf.beat_schedule = {
    "fetch-nist-data-every-10-seconds": {
        "task": "monitoring.tasks.fetch_nist_data_task",
        "schedule": 10.0,  # Executa a cada 10 segundos
    },
}

# EOF
