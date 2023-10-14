from django.db import models


class StateMultipliers(models.Model):
    name = models.CharField(max_length=20)
    monthly_tax = models.FloatField()
    flood_coverage = models.FloatField()


class StateAdditions(models.Model):
    name = models.CharField(max_length=20)
    coverage = models.BooleanField()


class Quotes(models.Model):
    monthly_subtotal = models.FloatField()
    monthly_taxes = models.FloatField()
