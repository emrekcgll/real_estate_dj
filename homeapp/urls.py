from django.urls import path
from homeapp import views

urlpatterns = [
    path("", views.index, name="h_index"),
]
