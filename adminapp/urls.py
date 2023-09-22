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
    path("get_county_by_city_id/<int:city_id>/", views.get_county_by_city_id, name="get_county_by_city_id"),
    path("get_region_by_county_id/<int:county_id>/", views.get_region_by_county_id, name="get_region_by_county_id"),


    path("update-owner/<int:pk>/", views.update_owner, name="update_owner")
]
