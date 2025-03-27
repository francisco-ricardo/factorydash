import factorydash  # This will set up the Django environment and logging

import pytest
from monitoring.models import MachineData
from django.utils.timezone import now

@pytest.mark.django_db
def test_machine_data_creation():
    """Test that a MachineData instance is created correctly."""
    data = MachineData.objects.create(
        machine_id="machine123",
        timestamp=now(),
        name="TestValue",
        value="123"
    )
    assert MachineData.objects.count() == 1
    assert data.id is not None
    assert data.machine_id == "machine123"
    assert data.name == "TestValue"
    assert data.value == "123"

# EOF
