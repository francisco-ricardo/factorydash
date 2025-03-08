import factorydash  # This will set up the Django environment

import os
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from monitoring.models import MachineData
from factorydash.settings import DATA_RETENTION_DAYS


class Command(BaseCommand):
    help = "Deletes records older than the configured retention period."

    def handle(self, *args, **kwargs) -> None:

        # Validate and parse the retention
        retention_days = os.getenv('DATA_RETENTION_DAYS', '2')
        try:
            retention_days = float(retention_days)
            if retention_days <= 0:
                raise ValueError("DATA_RETENTION_DAYS must be a positive number")
        except ValueError as e:
            raise ValueError(f"Invalid DATA_RETENTION_DAYS: {e}. Must be a positive number.")

        cutoff_date = now() - timedelta(days=retention_days)
        deleted_count, _ = MachineData.objects.filter(timestamp__lt=cutoff_date).delete()
        factorydash.logger.info(f"Deleted {deleted_count} records older than {retention_days} days from MachineData.")

# EOF
