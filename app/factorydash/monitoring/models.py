from django.db import models

# Create your models here.

from django.db import models

class MachineData(models.Model):
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
        db_table = "machinedata"
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['data_item_id']),
        ]

    def __str__(self):
        return f"{self.name} - {self.value} ({self.timestamp})"
