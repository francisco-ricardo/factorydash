from datetime import timedelta
from django.core.management.base import BaseCommand
from monitoring.models import MachineData
from django.utils.timezone import now
from factorydash.settings import DATA_RETENTION_DAYS
import logging

logger = logging.getLogger("factorydash")

class Command(BaseCommand):
    help = "Deletes records older than the configured retention period."

    def handle(self, *args, **kwargs) -> None:
        cutoff_date = now() - timedelta(days=DATA_RETENTION_DAYS)
        deleted_count, _ = MachineData.objects.filter(timestamp__lt=cutoff_date).delete()
        logger.info(f"Deleted {deleted_count} old records from MachineData.")
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} records older than {DATA_RETENTION_DAYS} days."))
