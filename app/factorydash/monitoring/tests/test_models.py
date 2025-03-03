import factorydash  # This will set up the Django environment and logging

import pytest
from monitoring.models import MachineData
from django.utils.timezone import now

@pytest.mark.django_db
def test_machine_data_creation():
    """Test that a MachineData instance is created correctly."""
    data = MachineData.objects.create(
        data_type="Events",
        data_item_id="test_123",
        timestamp=now(),
        name="TestEvent",
        value="Running"
    )
    assert MachineData.objects.count() == 1
    assert data.id is not None
    assert data.data_type == "Events"
    assert data.name == "TestEvent"
    assert data.value == "Running"

# EOF
