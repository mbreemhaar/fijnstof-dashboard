from django.contrib import admin

from municipalities import models


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(models.Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'province')
    list_filter = ('province',)
    search_fields = ('name', 'code')
