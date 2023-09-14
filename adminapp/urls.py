from django.urls import path
from adminapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("import_country/",views.import_country, name="import_country"),
    path("import_city/", views.import_city, name="import_city"),
    path("import_region/", views.import_region, name="import_region"),
    path("import_neighbourhood/", views.import_neighbourhood, name="import_neighbourhood"),

]
