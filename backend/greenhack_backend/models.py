from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.
class Temperature(models.Model):
    datetime = models.DateTimeField()
    reading = models.DecimalField(decimal_places=5,max_digits=10)

class Pressure(models.Model):
    datetime = models.DateTimeField()
    reading = models.DecimalField(decimal_places=5,max_digits=10)

class Humidity(models.Model):
    datetime = models.DateTimeField()
    reading = models.DecimalField(decimal_places=5,max_digits=10)