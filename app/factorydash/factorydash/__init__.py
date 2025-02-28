"""
This module sets up the Django environment, logging, and Celery for the 
factorydash project.

It ensures that the Django settings are configured, logging is set up, 
and the Celery app is always imported when Django starts.
"""

from __future__ import absolute_import, unicode_literals
import os
import sys


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
import logging
logger = logging.getLogger("factorydash")


# Set up Celery
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
__all__ = ('celery_app',)

# EOF
