from django.urls import path
from adminapp import views

urlpatterns = [
    path("", views.index, name="index"),


    path("estates/", views.estates, name="estates"),
    path("estate-create/", views.estate_create, name="estate_create"),


    path("estate_list_ajax/", views.estate_list_ajax, name="estate_list_ajax"),
]
