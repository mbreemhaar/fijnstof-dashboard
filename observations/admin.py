from django.contrib import admin

from observations.models import Sensor


# Register your models here.
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = [
        'sensor_community_id',
        'latitude',
        'longitude',
        'municipality',
    ]
