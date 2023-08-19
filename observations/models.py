from django.db import models
from django.utils.translation import gettext as _
from django_admin_geomap import GeoItem

from municipalities.models import Municipality


class Sensor(models.Model, GeoItem):
    sensor_community_id = models.IntegerField(unique=True)

    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)

    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='sensors'
    )

    @property
    def geomap_longitude(self):
        return '' if self.longitude is None else str(self.longitude)

    @property
    def geomap_latitude(self):
        return '' if self.latitude is None else str(self.latitude)

    def __str__(self):
        return str(self.sensor_community_id)

    def save(self, *args, **kwargs):
        if self.municipality is None:
            self.municipality = Municipality.from_coordinates(self.latitude, self.longitude)
        super().save(*args, **kwargs)


class Observation(models.Model):
    class ObservationType(models.TextChoices):
        PM25 = 'pm25', 'PM2,5'
        PM10 = 'pm10', 'PM10'
        RH = 'rh', _('Relative humidity')
        TEMP = 'temp', _('Temperature')

    timestamp = models.DateTimeField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=ObservationType.choices)
    value = models.DecimalField(max_digits=6, decimal_places=3)

    def human_readable_value(self):
        if self.type == 'temp':
            unit = '°C'
        elif self.type == 'rh':
            unit = '%'
        else:
            unit = ' μg/m3'

        return str(round(self.value)) + unit

    def __str__(self):
        return f'{self.timestamp} {self.human_readable_value()} ({self.get_type_display()})'
