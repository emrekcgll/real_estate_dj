from django.urls import path
from superuserapp import views

urlpatterns = [
    path("deneme/", views.deneme),
    path("", views.dashboard, name="dashboard"),
    path("estate-list/", views.estate_list, name="estate_list"),




    path("estate-agents/",views.estate_agents ,name="estate_agents"),
    path("get-manager/<int:pk>/",views.get_manager ,name="get_manager"),
    path("create-manager/",views.create_manager ,name="create_manager"),



    path("estate-offices/",views.estate_offices ,name="estate_offices"),
    path("get-office/<int:pk>/", views.group_details, name="group_details"),
    path("create-office/", views.create_group, name="create_group"),
    path("update-office/", views.update_group, name="update_group"),
    path("delete-office/", views.delete_group, name="delete_group"),


    path("import-operations/", views.import_operations, name="import_operations"),
    path("default-value/", views.default_value, name="default_value"),
    path("import_address_data/",views.import_address_data, name="import_address_data"),


    path("create_estate_type/", views.create_estate_type, name="create_estate_type"),
    path("create_estate_status/", views.create_estate_status, name="create_estate_status"),
    path("create_from_who/", views.create_from_who, name="create_from_who"),
    path("create_room_count/", views.create_room_count, name="create_room_count"),


    path("show_estate_type/", views.show_estate_type, name="show_estate_type"),
    path("show_estate_status/", views.show_estate_status, name="show_estate_status"),
    path("show_from_who/", views.show_from_who, name="show_from_who"),
    path("show_room_count/", views.show_room_count, name="show_room_count"),


    path("delete_estate_type/<int:pk>/", views.delete_estate_type, name="delete_estate_type"),
    path("delete_estate_status/<int:pk>/", views.delete_estate_status, name="delete_estate_status"),
    path("delete_from_who/<int:pk>/", views.delete_from_who, name="delete_from_who"),
    path("delete_room_count/<int:pk>/", views.delete_room_count, name="delete_room_count"),


    path("update_estate_type/<int:pk>/", views.update_estate_type, name="update_estate_type"),
    path("update_estate_status/<int:pk>/", views.update_estate_status, name="update_estate_status"),
    path("update_from_who/<int:pk>/", views.update_from_who, name="update_from_who"),
    path("update_room_count/<int:pk>/", views.update_room_count, name="update_room_count"),
]
