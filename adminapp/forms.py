from django import forms

from adminapp.models import RealEstate


class RealEstateForm(forms.ModelForm):
    class Meta:
        model = RealEstate
        fields = ("title", "room_count", "bathrooms_count", "m2_brut", "m2_net", "building_years", "building_floor", "is_balcony",
                  "estate_status", "estate_type", "from_who", "county", "region",
                  "city", "address", "using_status", "is_with_firniture",
                  "deed_status", "is_available_for_loan", "change", "dues", "description",)
        labels = {"title": "Başlık",
                  "room_count": "Oda Sayısı",
                  "bathrooms_count": "Banyo Sayısı",
                  "m2_brut": "Brüt m2",
                  "m2_net": "Net m2",
                  "building_years": "Bina Yaşı",
                  "building_floor": "Kat",
                  "is_balcony": "Balkon",
                  "estate_status": "Mülk Tipi",
                  "estate_type": "Emlak Durumu",
                  "from_who": "Kimden",
                  "city": "İl",
                  "county": "İlçe",
                  "region": "Mahalle",
                  "address":"Adres",
                  "using_status": "Kullanım Durumu",
                  "is_with_firniture": "Eşya",
                  "deed_status": "Tapu Durumu",
                  "is_available_for_loan": "Kredi Durumu",
                  "change": "Takas",
                  "dues": "Aidat",
                  "description": "Açıklama"}
        widgets = {"title": forms.TextInput(attrs={"class":"form-control"}),
                   "room_count": forms.Select(attrs={"class":"form-control"}),
                   "bathrooms_count": forms.NumberInput(attrs={"class":"form-control"}),
                   "m2_brut": forms.NumberInput(attrs={"class":"form-control"}),
                   "m2_net": forms.NumberInput(attrs={"class":"form-control"}),
                   "building_years": forms.NumberInput(attrs={"class":"form-control"}),
                   "building_floor": forms.TextInput(attrs={"class":"form-control"}),
                   "is_balcony": forms.NullBooleanSelect(attrs={"class":"form-control"}),
                   "estate_status": forms.Select(attrs={"class":"form-control"}),
                   "estate_type": forms.Select(attrs={"class":"form-control"}),
                   "from_who": forms.Select(attrs={"class":"form-control"}),
                   "city": forms.Select(attrs={"class":"form-control"}),
                   "county": forms.Select(attrs={"class":"form-control"}),
                   "region": forms.Select(attrs={"class":"form-control"}),
                   "address": forms.TextInput(attrs={"class":"form-control"}),
                   "using_status": forms.TextInput(attrs={"class":"form-control"}),
                   "is_with_firniture": forms.NullBooleanSelect(attrs={"class":"form-control"}),
                   "deed_status": forms.TextInput(attrs={"class":"form-control"}),
                   "is_available_for_loan": forms.NullBooleanSelect(attrs={"class":"form-control"}),
                   "change": forms.NullBooleanSelect(attrs={"class":"form-control"}),
                   "dues": forms.NumberInput(attrs={"class":"form-control"}),
                   "description": forms.Textarea(attrs={"class":"form-control"})}
