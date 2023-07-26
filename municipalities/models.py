from django.db import models


class Province(models.Model):
    """A province that has an official code and name, as specified by the Dutch Centraal Bureau voor de Statistiek."""
    code = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=255)

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
        ordering = ('province__name', 'name')
        indexes = [
            models.Index(fields=('name',)),
            models.Index(fields=('code',)),
            models.Index(fields=('province',))
        ]

        verbose_name_plural = 'municipalities'

    def __str__(self):
        return self.name
