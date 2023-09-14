from django.db import models

# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=30)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city_name = models.CharField(max_length=30)


class Region(models.Model):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    region_name = models.CharField(max_length=50)


class Neighbourhood(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    neighbourhood_name = models.CharField(max_length=50)
    neighbourhood_zip = models.CharField(max_length=10)


class Address(models.Model):
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=500)

