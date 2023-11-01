from django.urls import path
from homeapp import views

urlpatterns = [
    path("", views.index, name="h_index"),
    path("estates/", views.h_estates, name="h_estates"),
    path("estate-details/<int:pk>/", views.h_estate_details, name="h_estate_details"),
]
