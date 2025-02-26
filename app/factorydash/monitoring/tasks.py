import factorydash  # This will set up the Django environment and logging

from celery import shared_task

from monitoring.data_loader import save_nist_data
from django.core.management import call_command


@shared_task
def fetch_nist_data_task() -> str:
    """Celery task to fetch and save data from the NIST API."""
    try:
        save_nist_data()
        factorydash.logger.info("Celery Task: Successfully fetched NIST API data")
        return "NIST API data fetched and stored."
    except Exception as e:
        factorydash.logger.error(f"Celery Task Error: {str(e)}")
        return "NIST API task failed."

@shared_task
def cleanup_task() -> str:
    try:
        call_command('cleanup')
        factorydash.logger.info("Celery Task: Successfully deleted old data")
        return "Successfully deleted old data"
    except Exception as e:
        factorydash.logger.error(f"Celery Task: Cleanup old data Task Error: {str(e)}")
        return "Cleanup old data Task Error."

# EOF
