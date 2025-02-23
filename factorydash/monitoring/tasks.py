from celery.schedules import crontab
from celery import Celery
from celery import shared_task
import logging

from monitoring.data_loader import save_nist_data


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


# EOF
