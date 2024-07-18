from django.db import models
from model_utils.models import TimeStampedModel

class LocationRequest(TimeStampedModel):
    address = models.TextField()
    formatted_address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=["address"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return self.formatted_address or self.address

    @property
    def point(self):
        return self.latitude, self.longitude
