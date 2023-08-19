from django.contrib import admin
import django_admin_geomap

from observations.models import Sensor, Observation


@admin.register(Sensor)
class SensorAdmin(django_admin_geomap.ModelAdmin):
    list_display = [
        'sensor_community_id',
        'latitude',
        'longitude',
        'municipality',
    ]

    search_fields = [
        'sensor_community_id',
        'municipality__name'
    ]

    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = [
        'timestamp',
        'sensor',
        'value',
        'type',
    ]
