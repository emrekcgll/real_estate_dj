from django import forms

from adminapp.models import RealEstate


class RealEstateForm(forms.ModelForm):
    class Meta:
        model = RealEstate
        fields = ("title", "room_count", "bathrooms_count", "m2_brut", "m2_net", "building_years", "building_floor", "is_balcony",
                  "estate_status", "estate_type", "from_who",
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
                  "using_status": "Kullanım Durumu",
                  "is_with_firniture": "Eşya",
                  "deed_status": "Tapu Durumu",
                  "is_available_for_loan": ";Kredi Durumu",
                  "change": "Takas",
                  "dues": "Aydat",
                  "description": "Açıklama"}
