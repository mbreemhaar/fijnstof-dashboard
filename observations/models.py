from django.db import models

from municipalities.models import Municipality


class Sensor(models.Model):
    sensor_community_id = models.IntegerField()

    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)

    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.municipality is None:
            self.municipality = Municipality.from_coordinates(self.latitude, self.longitude)
        super().save(*args, **kwargs)
