from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    class Meta:
        abstract = True


class CustomGroup(BaseModel, Group):
    phone = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='group_images/', null=True, blank=True)
    class Meta:
        db_table = 'auth_group_additional'
        ordering = ["-created_at"]


class CustomUser(User):
    is_member = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    phone = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    class Meta:
        db_table = 'auth_user_additional'
        ordering = ["-date_joined"]


class City(models.Model): # il
    city_name = models.CharField(max_length=30)
    def __str__(self):
        return self.city_name


class County(models.Model): # ilçe
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    county_name = models.CharField(max_length=30)
    def __str__(self):
        return self.county_name


class Region(models.Model): # semt
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    region_name = models.CharField(max_length=30)
    def __str__(self):
        return self.region_name


class EstateType(models.Model):
    estate_type = models.CharField(max_length=30, unique=True) # Daire, Villa, Residance 
    def __str__(self):
        return self.estate_type


class EstateStatus(models.Model):
    estate_status = models.CharField(max_length=30, unique=True) # Satılık, Kiralık
    def __str__(self):
        return self.estate_status


class FromWho(models.Model):
    from_who = models.CharField(max_length=30, unique=True) # kimden, emlakcıdan, sahibinden
    def __str__(self):
        return self.from_who


class RoomCount(models.Model):
    room_count = models.CharField(max_length=10, unique=True) # oda sayısı
    def __str__(self):
        return self.room_count


class EstateOwner(BaseModel):
    name_surname = models.CharField(max_length=200)
    identity_number = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)


class EstateRenter(BaseModel):
    name_surname = models.CharField(max_length=200)
    identity_number = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)


class EstateBuyer(BaseModel):
    name_surname = models.CharField(max_length=200)
    identity_number = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)


class Contrat(BaseModel):
    contract_start_date = models.DateTimeField(auto_now_add=True)
    contract_duration = models.PositiveIntegerField()
    year_rental_price = models.PositiveIntegerField()
    mounth_rental_price = models.PositiveIntegerField()
    rent_payment_method = models.CharField(max_length=200)
    how_to_use_the_rented_property = models.CharField(max_length=200)
    status_of_the_rented_property = models.CharField(max_length=200)
    fixtures_delivered_with_the_rental = models.CharField(max_length=200)


class RealEstate(BaseModel):
    estate_owner = models.ForeignKey(EstateOwner, on_delete=models.SET_NULL, null=True, blank=True)
    estate_renter = models.ForeignKey(EstateRenter, on_delete=models.SET_NULL, null=True, blank=True)
    estate_buyer = models.ForeignKey(EstateBuyer, on_delete=models.SET_NULL, null=True, blank=True)
    estate_rent_contrat = models.ForeignKey(Contrat, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    estate_type = models.ForeignKey(EstateType, on_delete=models.SET_NULL, null=True, blank=True)
    estate_status = models.ForeignKey(EstateStatus, on_delete=models.SET_NULL, null=True, blank=True)
    from_who = models.ForeignKey(FromWho, on_delete=models.SET_NULL, null=True, blank=True) 
    room_count = models.ForeignKey(RoomCount, on_delete=models.SET_NULL, null=True, blank=True)

    apartment_number = models.CharField(max_length=10) # daire numarası
    exterior_door_number = models.CharField(max_length=10) # dış kapı numarası
    address = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    slug = models.SlugField(max_length=300, db_index=True)
    description = models.CharField(max_length=1000)
    estate_number = models.CharField(max_length=10) # GUID ID
    m2_brut = models.PositiveIntegerField() 
    m2_net = models.PositiveIntegerField() 
    heating = models.CharField(max_length=100) # ısıtma şekli
    using_status = models.CharField(max_length=10, null=True, blank=True) # kullanım durumu
    building_years = models.PositiveSmallIntegerField() # bina yaşı
    building_floor = models.PositiveSmallIntegerField() # bina katı
    location_floor = models.IntegerField() # bulunduğu kat
    bathrooms_count = models.CharField(max_length=10) # banyo sayısı
    within_site = models.BooleanField(default=False) # site içerisinde mi
    site_name = models.CharField(max_length=75, null=True, blank=True) # site adı
    is_with_firniture = models.BooleanField(default=False) # eşyalı mi
    dues = models.CharField(max_length=10) # aidat
    is_available_for_loan = models.BooleanField(default=True) # krediye uygun mu
    is_balcony = models.BooleanField(default=True) # balkon var mı
    deed_status = models.CharField(max_length=100) # tapu durumu
    change = models.BooleanField(default=False) # takas

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-pk"]


class RealEstateAgentCommission(BaseModel):
    estate = models.ForeignKey(RealEstate, on_delete=models.SET_NULL, null=True, blank=True)
    comission = models.PositiveIntegerField()


class Image(models.Model):
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="estate_images/")