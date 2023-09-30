from accountapp import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.account_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]