from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model


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
    class TypeChoices(models.TextChoices):
        DAIRE = 'DAIRE', 'Daire'
        VILLA = 'VILLA', 'Villa'
        RESIDENCE = 'RESIDENCE', 'Residence'
        MUSTAKIL_EV = 'MUSTAKIL_EV', 'Müstakil Ev'
    
    estate_type = models.CharField(max_length=30, unique=True, choices=TypeChoices.choices) # Daire, Villa, Residance 
    def __str__(self):
        return self.estate_type

class EstateStatus(models.Model):
    class StatusChoices(models.TextChoices):
        SATILIK = 'SATILIK', 'Satılık'
        KIRALIK = 'KIRALIK', 'Kiralık'

    estate_status = models.CharField(max_length=30, unique=True, choices=StatusChoices.choices) # Satılık, Kiralık
    def __str__(self):
        return self.estate_status

class FromWho(models.Model):
    class WhoChoices(models.TextChoices):
        EMLAKCIDAN = 'EMLAKCIDAN', 'Emlakçıdan'
        SAHIBINDEN = 'SAHIBINDEN', 'Sahibinden'

    from_who = models.CharField(max_length=30, unique=True, choices=WhoChoices.choices) # kimden, emlakcıdan, sahibinden
    def __str__(self):
        return self.from_who

class RoomCount(models.Model):
    class RoomChoices(models.TextChoices):
        BIR_SIFIR = '1+0', '1+0'
        BIR_BIR   = '1+1', '1+1'
        IKI_BIR   = '2+1', '2+1'
        IKI_SIFIR = '2+0', '2+0'
        UC_BIR    = '3+1', '3+1'
        UC_IKI    = '3+2', '3+2'
        UC_SIFIR  = '3+0', '3+0'
        DORT_BIR  = '4+1', '4+1'
        DORT_IKI  = '4+2', '4+2'
        BES_BIR   = '5+1', '5+1'
        BES_IKI   = '5+2', '5+2'

    room_count = models.CharField(max_length=10, unique=True, choices=RoomChoices.choices) # oda sayısı
    def __str__(self):
        return self.room_count


class EstateOwner(models.Model):
    name_surname = models.CharField(max_length=200)
    identity_number = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)

class EstateRenter(models.Model):
    name_surname = models.CharField(max_length=200)
    identity_number = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)

class EstateBuyer(models.Model):
    name_surname = models.CharField(max_length=200)
    identity_number = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)

class Contrat(models.Model):
    contract_start_date = models.DateTimeField(auto_now_add=True)
    contract_duration = models.PositiveIntegerField()
    year_rental_price = models.PositiveIntegerField()
    mounth_rental_price = models.PositiveIntegerField()
    rent_payment_method = models.CharField(max_length=200)
    how_to_use_the_rented_property = models.CharField(max_length=200)
    status_of_the_rented_property = models.CharField(max_length=200)
    fixtures_delivered_with_the_rental = models.CharField(max_length=200)


class RealEstate(models.Model):
    estate_owner = models.ForeignKey(EstateOwner, on_delete=models.SET_NULL, null=True, blank=True)
    estate_renter = models.ForeignKey(EstateRenter, on_delete=models.SET_NULL, null=True, blank=True)
    estate_buyer = models.ForeignKey(EstateBuyer, on_delete=models.SET_NULL, null=True, blank=True)
    estate_rent_contrat = models.ForeignKey(Contrat, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    estate_type = models.ForeignKey(EstateType, on_delete=models.SET_NULL, null=True, blank=True, choices=EstateType.TypeChoices.choices)
    estate_status = models.ForeignKey(EstateStatus, on_delete=models.SET_NULL, null=True, blank=True, choices=EstateStatus.StatusChoices.choices)
    from_who = models.ForeignKey(FromWho, on_delete=models.SET_NULL, null=True, blank=True, choices=FromWho.WhoChoices.choices) 
    room_count = models.ForeignKey(RoomCount, on_delete=models.SET_NULL, null=True, blank=True, choices=RoomCount.RoomChoices.choices)

    apartment_number = models.CharField(max_length=10) # daire numarası
    exterior_door_number = models.CharField(max_length=10) # dış kapı numarası
    address = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    slug = models.SlugField(max_length=300, db_index=True)
    description = models.CharField(max_length=1000)
    estate_number = models.CharField(max_length=10) # GUID ID
    created_date = models.DateField(auto_now_add=True)
    m2_brut = models.CharField(max_length=10) 
    m2_net = models.CharField(max_length=10) 
    heating = models.CharField(max_length=100) # ısıtma şekli
    using_status = models.CharField(max_length=10, null=True, blank=True) # kullanım durumu
    building_years = models.CharField(max_length=10) # bina yaşı
    building_floor = models.CharField(max_length=10) # bina katı
    location_floor = models.CharField(max_length=10) # bulunduğu kat
    bathrooms_count = models.CharField(max_length=10) # banyo sayısı
    within_site = models.BooleanField(default=False) # site içerisinde mi
    site_name = models.CharField(max_length=75, null=True, blank=True) # site adı
    is_with_firniture = models.BooleanField(default=False) # eşyalı mi
    dues = models.CharField(max_length=10) # aidat
    is_available_for_loan = models.BooleanField(default=False) # krediye uygun mu
    is_balcony = models.BooleanField(default=False) # balkon var mı
    deed_status = models.CharField(max_length=100) # tapu durumu
    change = models.BooleanField(default=False) # takas

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class RealEstateAgentCommission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    estate = models.ForeignKey(RealEstate, on_delete=models.SET_NULL, null=True, blank=True)
    comission = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="estate_images/")