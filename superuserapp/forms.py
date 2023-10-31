from django import forms
from adminapp.models import EstateStatus, EstateType, FromWho, RoomCount


class EstateTypeForm(forms.ModelForm):
    class Meta:
        model = EstateType
        fields = ("estate_type",)
        labels = {"estate_type": "Emlak Tipi"}
        widgets = {"estate_type": forms.TextInput(attrs={"class": "form-control"})}


class EstateStatusForm(forms.ModelForm):
    class Meta:
        model = EstateStatus
        fields = ("estate_status",)
        labels = {"estate_status": "Emlak Statüsü"}
        widgets = {"estate_status": forms.TextInput(attrs={"class": "form-control"})}


class FromWhoForm(forms.ModelForm):
    class Meta:
        model = FromWho
        fields = ("from_who",)
        labels = {"from_who": "Satıcı"}
        widgets = {"from_who": forms.TextInput(attrs={"class": "form-control"})}


class RoomCountForm(forms.ModelForm):
    class Meta:
        model = RoomCount
        fields = ("room_count",)
        labels = {"room_count": "Oda Sayısı"}
        widgets = {"room_count": forms.TextInput(attrs={"class": "form-control"})}
