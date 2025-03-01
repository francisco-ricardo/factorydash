import pytest
from unittest.mock import patch
from monitoring.tasks import cleanup_task

@pytest.mark.django_db
def test_cleanup_task():
    """Test that the cleanup Celery task correctly calls 'call_command("cleanup")'."""

    with patch("django.core.management.call_command") as mock_call:
        print("Starting cleanup_task test...")
        result = cleanup_task()
        print("cleanup_task result:", result)
        print("mock_call.call_count:", mock_call.call_count)
        
        mock_call.assert_called_once_with("cleanup")
        assert result == "Successfully deleted old data."