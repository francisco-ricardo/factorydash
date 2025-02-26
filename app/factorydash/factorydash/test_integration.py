import factorydash  # This will set up the Django environment and logging

from django.test import TestCase
from django.db import connections
from django.core.cache import cache
from celery import Celery


class FactoryDashIntegrationTests(TestCase):
    def test_database_connection(self):
        try:
            connections['default'].cursor()
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_redis_connection(self):
        try:
            cache.set('test_key', 'test_value', timeout=1)
            cache.get('test_key')
        except Exception as e:
            self.fail(f"Redis connection failed: {e}")

    def test_celery_connection(self):
        app = Celery('factorydash')
        app.config_from_object('django.conf:settings', namespace='CELERY')
        try:
            app.send_task('celery.ping')
        except Exception as e:
            self.fail(f"Celery connection failed: {e}")


# EOF