from django.urls import path
from adminapp import views

urlpatterns = [
    path("", views.index, name="index"),

    path("estates/", views.estates, name="estates"),
    path("estate/<int:pk>/", views.estate_details, name="estate_details"),
    path("estate-create/", views.estate_create, name="estate_create"),
    path("estate-update/<int:pk>/", views.estate_update, name="estate_update"),
    path("estate-delete/<int:pk>/", views.estate_delete, name="estate_delete"),
    
    path("estate_list_ajax/", views.estate_list_ajax, name="estate_list_ajax"),
    path("non_rental_estate_list_ajax/", views.non_rental_estate_list_ajax, name="non_rental_estate_list_ajax"),
    path("rental_estate_list_ajax/", views.rental_estate_list_ajax, name="rental_estate_list_ajax"),
    path("get_county_by_city_id/<int:city_id>/", views.get_county_by_city_id, name="get_county_by_city_id"),
    path("get_region_by_county_id/<int:county_id>/", views.get_region_by_county_id, name="get_region_by_county_id"),
    
    path("owners/", views.owners, name="owners"),
    path("owner/<int:pk>/", views.owner_details, name="owner_details"),
    path("owner-create/", views.owner_create, name="owner_create"),
    path("owner-update/<int:pk>/", views.owner_update, name="owner_update"),
    path("owner-delete/<int:pk>/", views.owner_delete, name="owner_delete"),

    path("renters/", views.renters, name="renters"),
    path("renter/<int:pk>/", views.renter_details, name="renter_details"),
    path("renter-create/<int:pk>/", views.renter_create, name="renter_create"),
    path("renter-update/<int:pk>/", views.renter_update, name="renter_update"),

    path("renter-delete/<int:pk>/", views.renter_delete, name="renter_delete"),
]
