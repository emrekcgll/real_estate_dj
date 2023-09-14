from django.urls import path
from adminapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("import_address_data/",views.import_address_data, name="import_address_data"),
]
