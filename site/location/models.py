from django.db import models


class Location(models.Model):
    city = models.CharField(
        verbose_name='Город',
        max_length=128,
        null=False,
        blank=False
    )

    street = models.CharField(
        verbose_name='Улица',
        max_length=128,
        null=False,
        blank=False
    )

    building = models.CharField(
        verbose_name='Дом',
        max_length=10,
        null=False,
        blank=False
    )

    office = models.SmallIntegerField(
        verbose_name='Квартира',
        null=True
    )

    metro = models.CharField(
        verbose_name='Метро',
        max_length=128,
        null=False,
        blank=False
    )

    def __str__(self):
        return f'{self.city}, {self.street}, {self.building}, {self.office}'
