"""
This module defines Celery tasks for the monitoring app in the factorydash project.

Tasks include fetching NIST machine data and cleaning up old records.
"""

import factorydash  # Sets up Django environment and logging

from celery import shared_task
from django.core.management import call_command


@shared_task
def load_nist_data_task() -> str:
    """
    Celery task to fetch and save data from the NIST API.

    Invokes the 'load_nist_data' management command to retrieve and store data.

    Returns:
        str: Status message indicating success or failure.
    """
    try:
        call_command('load_nist_data')        
    except Exception as e:
        factorydash.logger.error(f"Celery Task Error: {str(e)}")
        return "NIST API task failed."
    else:
        factorydash.logger.info("Celery Task: Successfully fetched NIST API data")
        return "NIST API data fetched and stored."


@shared_task
def cleanup_task() -> str:
    """
    Celery task to remove old machine data based on retention settings.

    Invokes the 'cleanup' management command to delete outdated records.

    Returns:
        str: Status message indicating success or failure.
    """    
    try:
        call_command('cleanup')        
    except Exception as e:
        factorydash.logger.error(f"Celery Task: Cleanup old data Task Error: {str(e)}")
        return "Cleanup old data Task Error."
    else:
        factorydash.logger.info("Celery Task: Successfully deleted old data")
        return "Successfully deleted old data."


# EOF
