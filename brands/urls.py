from django.urls import path

from . import views

app_name = 'brands'

urlpatterns = [
    path('branding', views.branding, name='branding'),
    path('brand_list', views.brand_list, name='brand_list'),
    path('create_brand', views.create_brand, name='create_brand'),
    path('brand_view/<str:brand_id>/', views.brand_view, name='brand_view'),
    path('delete_brand/<str:pk>/', views.delete_brand, name='delete_brand'),
    path('view_brands/', views.view_brands, name='view_brands'),
    ]