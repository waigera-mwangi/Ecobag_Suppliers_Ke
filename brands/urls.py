from django.urls import path

from . import views

app_name = 'brands'

urlpatterns = [
    path('custom_branding', views.custom_branding, name='custom_branding'),
    path('branding', views.branding, name='branding'),
    ]