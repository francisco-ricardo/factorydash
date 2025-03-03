import factorydash  # Ensure Django settings are loaded

from unittest.mock import patch

from monitoring.tasks import cleanup_task


# Test: Logging Mechanism
@patch("factorydash.logger.info")
def test_logging(mock_logger):
    """Ensure Celery task logs messages correctly."""

    with patch("monitoring.tasks.call_command") as mock_call:

        cleanup_task()    
        # Validate that logging was called
        mock_logger.assert_called()


# EOF