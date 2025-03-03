import factorydash  # This will set up the Django environment and logging

import pytest
from django.core.management import call_command
from monitoring.models import MachineData

@pytest.mark.django_db
def test_load_nist_data(mocker):
    """Test if NIST data is loaded successfully."""

    call_command("load_nist_data")
    assert MachineData.objects.count() > 0  # Ensure data is inserted

# EOF
