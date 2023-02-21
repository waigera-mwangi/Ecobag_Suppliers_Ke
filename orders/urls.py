from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.placeorder, name='placeorder'),
    path('checkout/', views.checkout, name='checkout'),
    path('view_orders/', views.view_orders, name='view_orders'),
]