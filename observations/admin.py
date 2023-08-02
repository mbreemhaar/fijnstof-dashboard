from django.contrib import admin

from observations.models import Sensor, Observation


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = [
        'sensor_community_id',
        'latitude',
        'longitude',
        'municipality',
    ]


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = [
        'timestamp',
        'sensor',
        'value',
        'type',
    ]
