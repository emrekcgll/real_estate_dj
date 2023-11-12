from django import forms
from adminapp.models import CustomGroup, CustomUser, EstateStatus, EstateType, FromWho, RoomCount


class UserForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    phone = forms.CharField(label="Phone")
    bio = forms.CharField(label="Bio", required=False)
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password" , widget=forms.PasswordInput)
    repassword = forms.CharField(label="Re-Password", widget=forms.PasswordInput)
    image = forms.ImageField(label="Profil Image", required=False)

    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        repassword = cleaned_data.get("repassword")
        phone = cleaned_data.get("phone")

        if username:
            try:
                user = CustomUser.objects.get(username=username)
                self.add_error("username", "This username is already exists.")
            except:
                pass

        if email:
            try:
                user = CustomUser.objects.get(email=email)
                self.add_error("email", "This email address is already exists.")
            except:
                pass

        if phone:
            try:
                user = CustomUser.objects.get(phone=phone)
                self.add_error("phone", "This number is already exists.")
            except:
                pass
                
        if password != repassword:
            self.add_error("password" ,"Password and Re-Password fields do not match.")
        
        return cleaned_data




class GroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ['name', 'phone', 'description', 'image']
        labels = {'name': 'Office Name',
                  'phone': 'Office Phone',
                  'description': 'Office Description',
                  'image': 'Estate Office Image'}

    def clean(self):
        cleaned_data = super().clean()

        name = self.cleaned_data['name']

        try:
            group = CustomGroup.objects.get(name=name)
            self.add_error("name", "This office is already exists.")
        except CustomGroup.DoesNotExist:
            pass

        return cleaned_data
    

# class GroupForm(forms.Form):
#     group_name = forms.CharField(label="Office Name")
#     group_phone = forms.CharField(max_length=11, label="Office Phone")
#     group_description = forms.CharField(label="Office Description")
#     group_image = forms.ImageField(label="Estate Office Image", required=False)

#     def clean(self):
#         cleaned_data = super().clean()
        
#         name = cleaned_data.get("name")

#         if name:
#             try:
#                 group = CustomGroup.objects.get(name=name)
#                 self.add_error("group_name", "This office is already exists.")
#             except:
#                 pass

#         return cleaned_data
    


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
