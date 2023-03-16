from django.urls import path

from . import views

app_name = 'supply'

urlpatterns = [
    path('request_supply/', views.create_supplyTender, name='request_supply'),
    path('create_supply/', views.create_supply, name='create_supply'),
    path('supply_list/', views.supply_list, name='supply_list'),
    path('supply_request_list/', views.supply_request_list, name='supply_request_list'),
    path('update_supply_request/<str:pk>/', views.update_supply_request, name='update_supply_request'),
    path('delete_supply_request/<str:pk>/', views.delete_supply_request, name='delete_supply_request'),
]