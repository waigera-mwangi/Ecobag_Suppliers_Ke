from delivery import views

from django.urls import path

from .views import *

app_name = "delivery"

urlpatterns = [
path('create_delivery/', views.create_delivery, name='create_delivery'),
path('delivery_list/', views.delivery_list, name='delivery_list'),
path('delivery_list_driver/', views.delivery_list_driver, name='delivery_list_driver'),
path('update_delivery/<str:pk>/', views.update_delivery, name='update_delivery'),
path('update_delivery_driver/<str:pk>/', views.update_delivery_driver, name='update_delivery_driver'),
path('delete_delivery/<str:pk>/', views.delete_delivery, name='delete_delivery'),
]