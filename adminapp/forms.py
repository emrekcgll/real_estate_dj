from django import forms
from adminapp.models import Contrat, EstateBuyer, EstateOwner, EstateRenter, RealEstate


class EstateRentForm(forms.ModelForm):
    class Meta:
        model = Contrat
        exclude = ["contract_start_date"]
        fields = ("contract_start_date", "contract_duration", 
                 "year_rental_price", "mounth_rental_price", 
                 "rent_payment_method", "how_to_use_the_rented_property", 
                 "status_of_the_rented_property", "fixtures_delivered_with_the_rental")
        labels = {"contract_start_date": "Akdin Başlangıç Tarihi", 
                  "contract_duration": "Akdin Başlangıç Süresi",
                  "year_rental_price": "Yıllık Kira Bedeli",
                  "mounth_rental_price": "Aylık Kira Bedeli",
                  "rent_payment_method":"Kira Bedelinin Ödeme Şekli", 
                  "how_to_use_the_rented_property": "Kiralananı Kullanım Şekli", 
                  "status_of_the_rented_property":"Kiralananın Durumu", 
                  "fixtures_delivered_with_the_rental": "Kiralananla Birlikte Teslim Edilen Demirbaşlar"}
        widgets = {"contract_start_date": forms.DateInput(attrs={"class": "form-control"}),
                   "contract_duration": forms.NumberInput(attrs={"class": "form-control", "placeholder":"Kira sözleşmesinin süresi"}),
                   "year_rental_price": forms.NumberInput(attrs={"class": "form-control", "placeholder":"Yıllık kira bedeli"}),
                   "mounth_rental_price": forms.NumberInput(attrs={"class": "form-control", "placeholder":"Aylık kira bedeli"}),
                   "rent_payment_method": forms.TextInput(attrs={"class": "form-control", "placeholder": "Her ayın beşinci günü akşamına kadar peşin olarak"}),
                   "how_to_use_the_rented_property": forms.TextInput(attrs={"class": "form-control", "placeholder":"Yalnızca mesken, (konut) olarak"}),
                   "status_of_the_rented_property": forms.TextInput(attrs={"class": "form-control", "placeholder":"Sağlam, tam, kullanılmaya elverişli, boyalı"}),
                   "fixtures_delivered_with_the_rental": forms.Textarea(attrs={"class": "form-control", "placeholder":".... marka kombi, doğalgaz sayaçları, kiralananın apartman kapısı ve daire kapısının ikişer adet anahtarı"})}


class EstateOwnerForm(forms.ModelForm):
    class Meta:
        model = EstateOwner
        fields = ("name_surname", "identity_number", "phone", "address")
        labels = {"name_surname": "Ad Soyad", "identity_number": "TC", "phone": "Telefon", "address": "Adres" }
        widgets = {"name_surname": forms.TextInput(attrs={"class": "form-control"}),
                   "identity_number": forms.TextInput(attrs={"class": "form-control"}),
                   "phone": forms.NumberInput(attrs={"class": "form-control"}),
                   "address": forms.TextInput(attrs={"class": "form-control"})}


class EstateRenterForm(forms.ModelForm):
    class Meta:
        model = EstateRenter
        fields = ("name_surname", "identity_number", "phone", "address")
        labels = {"name_surname": "Ad Soyad", "identity_number": "TC", "phone": "Telefon", "address": "Adres" }
        widgets = {"name_surname": forms.TextInput(attrs={"class": "form-control"}),
                   "identity_number": forms.TextInput(attrs={"class": "form-control"}),
                   "phone": forms.NumberInput(attrs={"class": "form-control"}),
                   "address": forms.TextInput(attrs={"class": "form-control"})}


class EstateBuyerForm(forms.ModelForm):
    class Meta:
        model = EstateBuyer
        fields = ("name_surname", "identity_number", "phone", "address")
        labels = {"name_surname": "Ad Soyad", "identity_number": "TC", "phone": "Telefon", "address": "Adres" }
        widgets = {"name_surname": forms.TextInput(attrs={"class": "form-control"}),
                   "identity_number": forms.TextInput(attrs={"class": "form-control"}),
                   "phone": forms.NumberInput(attrs={"class": "form-control"}),
                   "address": forms.TextInput(attrs={"class": "form-control"})}


class RealEstateForm(forms.ModelForm):
    VAR_YOK_CHOICES = (('True', 'Var'), ('False', 'Yok'))
    EVET_HAYIR_CHOICES = (('True', 'Evet'),('False', 'Hayır'))
    
    is_balcony = forms.ChoiceField(
        label="Balkon",
        choices=VAR_YOK_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'checkbox-input'}),  
    )

    is_with_firniture = forms.ChoiceField(
        label="Eşya",
        choices=VAR_YOK_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'checkbox-input'}),  
    )

    within_site = forms.ChoiceField(
        label="Site İçerisinde",
        choices=EVET_HAYIR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'checkbox-input'}),  
    )

    is_available_for_loan = forms.ChoiceField(
        label="Krediye Uygun",
        choices=EVET_HAYIR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'checkbox-input'}),
    )

    change = forms.ChoiceField(
        label="Takas",
        choices=VAR_YOK_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'checkbox-input'}),
    )


    class Meta:
        model = RealEstate
        fields = ("title", "room_count", "bathrooms_count", "m2_brut", "m2_net", "building_years", "building_floor",
                  "estate_status", "estate_type", "from_who", "county", "region", "heating", "price", "site_name",
                  "city", "address", "using_status", "location_floor", "estate_owner",
                  "deed_status","dues", "description", "apartment_number", "exterior_door_number")
        labels = {"title": "Başlık", "room_count": "Oda Sayısı", "bathrooms_count": "Banyo Sayısı", "estate_owner": "Mülk Sahibi", "m2_brut": "Brüt m2", "m2_net": "Net m2",
                  "site_name": "Site Adı", "heating": "Isıtma", "building_years": "Bina Yaşı", "price": "Fiyat", "building_floor": "Kat", "location_floor": "Bulunduğu Kat",
                  "estate_status": "Mülk Tipi", "estate_type": "Emlak Durumu", "from_who": "Kimden", "city": "İl", "county": "İlçe",
                  "region": "Mahalle", "address": "Adres", "using_status": "Kullanım Durumu",
                  "deed_status": "Tapu Durumu", "dues": "Aidat", "description": "Açıklama", "apartment_number": "Daire Numarası", "exterior_door_number": "Dış Kapı Numarası"}
        widgets = {"title": forms.TextInput(attrs={"class": "form-control"}),
                   "room_count": forms.Select(attrs={"class": "form-control"}),
                   "bathrooms_count": forms.NumberInput(attrs={"class": "form-control"}),
                   "price": forms.NumberInput(attrs={"class": "form-control"}),
                   "m2_brut": forms.NumberInput(attrs={"class": "form-control"}),
                   "m2_net": forms.NumberInput(attrs={"class": "form-control"}),
                   "building_years": forms.NumberInput(attrs={"class": "form-control"}),
                   "building_floor": forms.NumberInput(attrs={"class": "form-control"}),
                   "location_floor": forms.NumberInput(attrs={"class": "form-control"}),
                   "estate_status": forms.Select(attrs={"class": "form-control"}),
                   "estate_type": forms.Select(attrs={"class": "form-control"}),
                   "from_who": forms.Select(attrs={"class": "form-control"}),
                   "city": forms.Select(attrs={"class": "form-control"}),
                   "county": forms.Select(attrs={"class": "form-control"}),
                   "region": forms.Select(attrs={"class": "form-control"}),
                   "address": forms.TextInput(attrs={"class": "form-control"}),
                   "using_status": forms.TextInput(attrs={"class": "form-control"}),
                   "deed_status": forms.TextInput(attrs={"class": "form-control"}),
                   "site_name": forms.TextInput(attrs={"class": "form-control"}),
                   "heating": forms.TextInput(attrs={"class": "form-control"}),
                   "dues": forms.NumberInput(attrs={"class": "form-control"}),
                   "description": forms.Textarea(attrs={"class": "form-control"}),
                   "apartment_number": forms.TextInput(attrs={"class": "form-control"}),
                   "exterior_door_number": forms.TextInput(attrs={"class": "form-control"})}
