import factorydash  # This will set up the Django environment

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from monitoring.models import MachineData
from factorydash.settings import DATA_RETENTION_DAYS


class Command(BaseCommand):
    help = "Deletes records older than the configured retention period."

    def handle(self, *args, **kwargs) -> None:
        cutoff_date = now() - timedelta(days=DATA_RETENTION_DAYS)
        deleted_count, _ = MachineData.objects.filter(timestamp__lt=cutoff_date).delete()
        factorydash.logger.info(f"Deleted {deleted_count} records older than {DATA_RETENTION_DAYS} days from MachineData.")

# EOF
