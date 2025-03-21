"""
This module defines the database models for the monitoring app in the 
factorydash project.

It includes the MachineData model, which stores data related to machine 
events and samples from NIST manufacturing data sources.
"""

from django.db import models
from typing import Optional


class MachineData(models.Model):
    """
    Model representing machine data, including events and samples.

    Attributes:
        data_type (str): The type of data, either 'Events' or 'Samples'.
        data_item_id (str): Unique identifier for the data item.
        timestamp (datetime.datetime): Timestamp when the data was recorded.
        name (Optional[str]): Name of the data item, if applicable.
        value (Optional[str]): Value of the data item, if applicable.
    """

    DATA_TYPES = [
        ('Events', 'Events'),
        ('Samples', 'Samples'),
    ]

    data_type: str = models.CharField(max_length=10, choices=DATA_TYPES)
    data_item_id: str = models.CharField(max_length=255)
    timestamp: models.DateTimeField = models.DateTimeField()
    name: Optional[str] = models.CharField(max_length=255, null=True, blank=True)
    value: Optional[str] = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        """
        Meta options for the MachineData model.

        Attributes:
            db_table (str): Custom database table name.
            indexes (list): Database indexes for query optimization.
        """
        db_table: str = "machinedata"
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['data_item_id']),
        ]

    def __str__(self):
        """
        Provides a string representation of the MachineData instance.

        Returns:
            str: A formatted string with name, value, and timestamp.

        """
        return f"{self.name} - {self.value} ({self.timestamp})"

# EOF
