from django.db import models
from django.utils.text import slugify


class City(models.Model): # il
    city_name = models.CharField(max_length=30)

    def __str__(self):
        return self.city_name


class County(models.Model): # ilçe
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    county_name = models.CharField(max_length=30)


class Region(models.Model): # semt
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    region_name = models.CharField(max_length=30)


class Neighbourhood(models.Model): # mahalle
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    neighbourhood_name = models.CharField(max_length=100)
    neighbourhood_zip = models.CharField(max_length=10)


class Address(models.Model):
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=500)


class EstateType(models.Model):
    estate_type = models.CharField(max_length=20, unique=True) # Daire, Villa, Residance 


class EstateStatus(models.Model):
    estate_status = models.CharField(max_length=20, unique=True) # Satılık, Kiralık 


class FromWho(models.Model):
    from_who = models.CharField(max_length=50, unique=True) # kimden, emlakcıdan, sahibinden


class RoomCount(models.Model):
    room_count = models.CharField(max_length=10, unique=True) # oda sayısı


class RealEstate(models.Model):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.SET_NULL, null=True, blank=True)
    estate_type = models.ForeignKey(EstateType, on_delete=models.SET_NULL, null=True, blank=True)
    estate_status = models.ForeignKey(EstateStatus, on_delete=models.SET_NULL, null=True, blank=True)
    from_who = models.ForeignKey(FromWho, on_delete=models.SET_NULL, null=True, blank=True) 
    room_count = models.ForeignKey(RoomCount, on_delete=models.SET_NULL, null=True, blank=True)


    address = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=300, db_index=True)
    description = models.CharField(max_length=1000)
    estate_number = models.CharField(max_length=10) # GUID ID
    created_date = models.DateField(auto_now_add=True)
    m2_brut = models.CharField(max_length=10) 
    m2_net = models.CharField(max_length=10) 
    using_status = models.CharField(max_length=10)
    building_years = models.CharField(max_length=10) # bina yaşı
    building_floor = models.CharField(max_length=10) # bina katı
    bathrooms_count = models.CharField(max_length=10) # banyo sayısı
    is_with_firniture = models.BooleanField(default=False) # eşyalı eşyasız
    dues = models.CharField(max_length=10) # aidat
    is_available_for_loan = models.BooleanField(default=False) # krediye uygun
    is_balcony = models.BooleanField(default=False)
    deed_status = models.CharField(max_length=100) # tapu durumu
    change = models.BooleanField(default=False) # takas

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
