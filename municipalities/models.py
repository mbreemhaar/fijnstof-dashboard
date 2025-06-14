from functools import lru_cache
from typing import Optional

from geopy import Nominatim, Location
from django.db import models
from geopy.exc import GeocoderUnavailable

from fijnstof.settings import NOMINATIM_USER_AGENT

_geolocator = Nominatim(user_agent=NOMINATIM_USER_AGENT)


class Province(models.Model):
    """A province that has an official code and name, as specified by the Dutch Centraal Bureau voor de Statistiek."""
    code = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('code',)
        indexes = [
            models.Index(fields=('name',)),
            models.Index(fields=('code',)),
        ]


class Municipality(models.Model):
    """
    A municipality that has an official code and name, as specified by the Dutch Centraal Bureau voor de Statistiek.
    Each municipality is also linked to the province that it is a part of.
    """
    code = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    class Meta:
        ordering = ('province__code', 'name')
        indexes = [
            models.Index(fields=('name',)),
            models.Index(fields=('code',)),
            models.Index(fields=('province',))
        ]

        verbose_name_plural = 'municipalities'

    @staticmethod
    @lru_cache
    def from_coordinates(latitude, longitude):
        try:
            location: Optional[Location] = _geolocator.reverse(f'{latitude},{longitude}')
        except GeocoderUnavailable:
            location = None

        if location is not None:
            try:
                for field_name in ['municipality', 'city', 'town', 'village']:
                    municipality_name = location.raw['address'].get(field_name)
                    if municipality_name is not None:
                        break
            except KeyError as e:
                raise Exception(f'No valid location found for ({latitude}, {longitude})') from e
            try:
                return Municipality.objects.get(name=municipality_name)
            except Municipality.DoesNotExist:
                return None
        else:
            return None

    def __str__(self):
        return self.name
