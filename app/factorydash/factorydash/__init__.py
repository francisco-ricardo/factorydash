import os
import sys
import logging


# Set up Django environment
if not getattr(sys, '_is_django_setup', False):
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_path not in sys.path:
        sys.path.append(project_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorydash.settings")
    import django
    django.setup()
    sys._is_django_setup = True


# Set up logging
logger = logging.getLogger("factorydash")


# Set up Celery
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

# EOF
