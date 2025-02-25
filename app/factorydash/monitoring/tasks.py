from celery import shared_task
import logging

from monitoring.data_loader import save_nist_data
#from monitoring.management.commands.cleanup_old_data import Command
from django.core.management import call_command


logger = logging.getLogger("factorydash")


@shared_task
def fetch_nist_data_task() -> str:
    """Celery task to fetch and save data from the NIST API."""
    try:
        save_nist_data()
        logger.info("Celery Task: Successfully fetched NIST API data")
        return "NIST API data fetched and stored."
    except Exception as e:
        logger.error(f"Celery Task Error: {str(e)}")
        return "NIST API task failed."

@shared_task
def cleanup_old_data_task():
    call_command('cleanup_old_data')

# @shared_task
# def cleanup_old_data_task():
#     try:
#         command = Command()
#         command.handle()
#         logger.info("Celery Task: Successfully deleted old data")
#         return "Successfully deleted old data"
#     except Exception as e:
#         logger.error(f"Celery Task: Cleanup old data Task Error: {str(e)}")
#         return "Cleanup old data Task Error."


# EOF
