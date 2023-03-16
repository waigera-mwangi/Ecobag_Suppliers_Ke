from django.urls import path

from . import views

app_name = 'supply'

urlpatterns = [
    path('request_supply/', views.create_supplyTender, name='request_supply'),
    path('create_supply/', views.create_supply, name='create_supply'),
    path('supply_request_list/', views.supply_request_list, name='supply_request_list'),
]