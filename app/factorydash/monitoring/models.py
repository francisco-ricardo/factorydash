"""
This module defines the database models for the monitoring app in the 
factorydash project.

It includes the MachineData model, which stores data related to machine 
events and samples.
"""

from django.db import models

# Create your models here.

from django.db import models

class MachineData(models.Model):
    """
    Model representing machine data, including events and samples.

    Attributes:
        data_type (str): The type of data (Events or Samples).
        data_item_id (str): The ID of the data item.
        timestamp (datetime): The timestamp of the data.
        name (str): The name of the data item (optional).
        value (str): The value of the data item (optional).
    """

    DATA_TYPES = [
        ('Events', 'Events'),
        ('Samples', 'Samples'),
    ]

    data_type = models.CharField(max_length=10, choices=DATA_TYPES)
    data_item_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        """
        Meta options for the MachineData model.
        
        Attributes:
            db_table (str): The name of the database table.
            indexes (list): A list of indexes for the model.
        """

        db_table = "machinedata"
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['data_item_id']),
        ]

    def __str__(self):
        """
        String representation of the MachineData model.
        
        Returns:
            str: A string representation of the machine data.
        """

        return f"{self.name} - {self.value} ({self.timestamp})"

# EOF
