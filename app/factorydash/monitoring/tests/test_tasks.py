import factorydash  # This will set up the Django environment and logging

import pytest
from unittest.mock import patch
from monitoring.tasks import cleanup_task
from monitoring.tasks import load_nist_data_task

@pytest.mark.django_db
def test_cleanup_task():
    """Test that the cleanup Celery task correctly calls 'call_command("cleanup")'."""

    with patch("monitoring.tasks.call_command") as mock_call:
        result = cleanup_task()
        mock_call.assert_called_once_with("cleanup")
        assert result == "Successfully deleted old data."


@pytest.mark.django_db
def test_load_nist_data_task():
    """Test that the cleanup Celery task correctly calls 'call_command("cleanup")'."""

    with patch("monitoring.tasks.call_command") as mock_call:
        result = load_nist_data_task()
        mock_call.assert_called_once_with("load_nist_data")
        assert result == "NIST API data fetched and stored."


# EOF