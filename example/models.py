# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property

from example.managers import CarManager


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Car(models.Model):
    CLASSIFICATION = (
        ('SEDAN', 'Sedan'),
        ('HATCH', 'Hatchback'),
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('CONVERT', 'Convertible'),
        ('SPORT', 'Sport'),
    )

    manufacturer = models.ForeignKey(Manufacturer)
    model = models.CharField(max_length=50)
    manufactured = models.DateField()
    classification = models.CharField(choices=CLASSIFICATION, max_length=10, blank=True)
    retail_price = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    is_bullet_proof = models.BooleanField(default=False)

    objects = CarManager()

    @cached_property
    def classification_display(self):
        return dict(self.CLASSIFICATION).get(self.classification, '')

    def __str__(self):
        return f'{self.manufacturer} - {self.model} {self.classification_display} ({self.manufactured.year})'

