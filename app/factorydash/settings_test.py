# settings_test.py (for pytest)
import os
from factorydash.settings import *

DEBUG = True

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True