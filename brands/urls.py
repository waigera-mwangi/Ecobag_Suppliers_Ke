from django.urls import path

from . import views

app_name = 'brands'

urlpatterns = [
    path('branding', views.branding, name='branding'), #Customer creating brand
    
    path('pending_brands/', views.pending_brand_list, name='pending_brands'), #Staff viewing pending brands in table
    path('approved_brands/', views.approved_brand_list, name='approved_brands'), #Staff viewing approved brands in table
    path('rejected_brands/', views.rejected_brand_list, name='rejected_brands'), #Staff viewing rejected brands in table
    path('complete_brands/', views.complete_brand_list, name='complete_brands'), #Staff viewing complete brands in table
    
    path('change_status/<int:pk>/<str:status>/', views.change_status, name='change_status'), #Changes the status of the brand
    path('create_brand', views.create_brand, name='create_brand'),
    path('brand_view/<str:brand_id>/', views.brand_view, name='brand_view'),
    path('delete_brand/<str:pk>/', views.delete_brand, name='delete_brand'),
    path('view_brands/', views.view_brands, name='view_brands'), #CUstomer viewing brands
    ]