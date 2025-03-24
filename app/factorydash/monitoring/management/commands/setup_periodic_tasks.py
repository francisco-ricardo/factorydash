"""
This module defines a Django management command to set up periodic Celery tasks.

It ensures that the necessary periodic tasks (load_nist_data_task, cleanup_task, 
update_dashboard) are created in the Celery Beat schedule.
"""
import factorydash  # Sets up Django environment and logging

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from monitoring.tasks import load_nist_data_task, cleanup_task, update_dashboard
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import json


class Command(BaseCommand):
    """
    Django management command to set up periodic Celery tasks.

    Ensures that the load_nist_data_task, cleanup_task, and update_dashboard 
    tasks are created in the Celery Beat schedule.
    """

    help: str = 'Sets up periodic tasks for Celery Beat'

    def handle(self, *args, **options) -> None:
        """
        Handles the execution of the setup_periodic_tasks command.

        Checks for and creates the necessary periodic tasks.
        """
        factorydash.logger.info('Setting up periodic tasks...')

        # Define the interval for the tasks
        load_nist_data_interval, _ = IntervalSchedule.objects.get_or_create(
            every=settings.LOAD_NIST_DATA_SCHEDULE_SECONDS,
            period=IntervalSchedule.SECONDS,
        )

        cleanup_interval, _ = IntervalSchedule.objects.get_or_create(
            every=settings.CLEANUP_OLD_DATA_SCHEDULE_HOURS,
            period=IntervalSchedule.HOURS,
        )

        update_dashboard_interval, _ = IntervalSchedule.objects.get_or_create(
            every=settings.UPDATE_DASHBOARD_SCHEDULE_SECONDS,
            period=IntervalSchedule.SECONDS,
        )

        # Define the tasks
        tasks_to_create = [
            {
                'name': 'Load NIST Data',
                'task': 'monitoring.tasks.load_nist_data_task',
                'interval': load_nist_data_interval,
                'enabled': True,
                'kwargs': {},
            },
            {
                'name': 'Cleanup Old Data',
                'task': 'monitoring.tasks.cleanup_task',
                'interval': cleanup_interval,
                'enabled': True,
                'kwargs': {},
            },
            {
                'name': 'Update Dashboard',
                'task': 'monitoring.tasks.update_dashboard',
                'interval': update_dashboard_interval,
                'enabled': True,
                'kwargs': {},
            },
        ]

        # Create the tasks if they don't exist
        for task_data in tasks_to_create:
            task_name = task_data['name']
            task = task_data['task']
            interval = task_data['interval']
            enabled = task_data['enabled']
            kwargs = task_data['kwargs']

            if not PeriodicTask.objects.filter(task=task).exists():
                PeriodicTask.objects.create(
                    name=task_name,
                    task=task,
                    interval=interval,
                    enabled=enabled,
                    kwargs=json.dumps(kwargs),
                    start_time=timezone.now() + timedelta(seconds=10),
                )
                factorydash.logger.info(f'Created periodic task: {task_name}')
                
            else:
                factorydash.logger.info(f'Periodic task already exists: {task_name}')

        factorydash.logger.info('Periodic tasks setup complete.')

# EOF
