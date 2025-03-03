# settings_test.py (for pytest)

from .settings import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "factorydash",
        "USER": "factorydash",
        "PASSWORD": "factorydash",
        "HOST": "localhost",
        "PORT": "5433",  # Must match the port in ci.yml
    }
}

CELERY_BROKER_URL = "redis://localhost:6380/0"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# EOF