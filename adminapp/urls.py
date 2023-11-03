from django.urls import path
from adminapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.user_profile, name="user_profile"),


    path("estates/", views.estates, name="estates"),
    path("estate/<int:pk>/", views.estate_details, name="estate_details"),
    path("estate-create/", views.estate_create, name="estate_create"),
    path("estate-update/<int:pk>/", views.estate_update, name="estate_update"),
    path("estate-delete/<int:pk>/", views.estate_delete, name="estate_delete"),
    

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


    path("estate-rent-contrats", views.estate_rent_contrats, name="estate_rent_contrats"),
    path("estate-rent-contrat-create/<int:pk>/", views.estate_rent_contrat_create, name="estate_rent_contrat_create"),
    path("estate-rent-contrat-update/<int:pk>/", views.estate_rent_contrat_update, name="estate_rent_contrat_update"),
    path("estate-rent-contrat-delete/<int:pk>/", views.estate_rent_contrat_delete, name="estate_rent_contrat_delete"),
    path("estate-rent-contrat-details/<int:pk>/", views.estate_rent_contrat_details, name="estate_rent_contrat_details"),
    path("estate_rent_contrat_pdf/<int:pk>/", views.estate_rent_contrat_pdf, name="estate_rent_contrat_pdf"),


    path("buyers/", views.buyers, name="buyers"),
    path("buyer/<int:pk>/", views.buyer_details, name="buyer_details"),
    path("buyer-create/<int:pk>/", views.buyer_create, name="buyer_create"),
    path("buyer-update/<int:pk>/", views.buyer_update, name="buyer_update"),
    path("buyer-delete/<int:pk>/", views.buyer_delete, name="buyer_delete"),


    path("get_county_by_city_id/<int:city_id>/", views.get_county_by_city_id, name="get_county_by_city_id"),
    path("get_region_by_county_id/<int:county_id>/", views.get_region_by_county_id, name="get_region_by_county_id"),
]
