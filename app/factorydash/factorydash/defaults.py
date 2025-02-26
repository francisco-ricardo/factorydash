import os
import sys
import django

def set_django_environment() -> None:
    """Set up Django environment for Celery"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorydash.settings")
    django.setup()

# EOF
