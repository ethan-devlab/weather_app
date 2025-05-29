# coding=utf-8
from django.urls import path
from . import views

# app_name = 'weather_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.sign_up, name="signup"),
    path('authentication', views.authentication, name="Authentication"),
    path('logout', views.log_out, name="Logout"),
    path('error', views.handler403, name="error"),
]