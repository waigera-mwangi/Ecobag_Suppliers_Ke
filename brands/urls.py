from django.urls import path

from . import views

app_name = 'brands'

urlpatterns = [
    path('custom_branding', views.custom_branding, name='custom_branding'),
    path('branding', views.branding, name='branding'),
    path('brand_list', views.brand_list, name='brand_list'),
    path('create_brand', views.create_brand, name='create_brand'),
    path('update_brand/<str:pk>/', views.update_brand, name='update_brand'),
    path('delete_brand/<str:pk>/', views.delete_brand, name='delete_brand'),
    
    ]