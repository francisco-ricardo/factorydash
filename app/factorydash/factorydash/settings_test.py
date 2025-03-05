# settings_test.py (for pytest)

from .settings import *

DEBUG = True

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# EOF