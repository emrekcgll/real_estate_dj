from django.urls import path
from modelapp import views

urlpatterns = [
    path("import-operations/", views.import_operations, name="import_operations"),
    path("import_address_data/",views.import_address_data, name="import_address_data"),



    path("create_estate_type/", views.create_estate_type, name="create_estate_type"),
    path("create_estate_status/", views.create_estate_status, name="create_estate_status"),
    path("create_from_who/", views.create_from_who, name="create_from_who"),
    path("create_room_count/", views.create_room_count, name="create_room_count"),
    
    path("show_estate_type/", views.show_estate_type, name="show_estate_type"),
    path("show_estate_status/", views.show_estate_status, name="show_estate_status"),
    path("show_from_who/", views.show_from_who, name="show_from_who"),
    path("show_room_count/", views.show_room_count, name="show_room_count"),
]
