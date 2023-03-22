from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.placeorder, name='placeorder'),
    path('checkout/', views.checkout, name='checkout'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('order_view <str:t_no>/',views.order_view, name='orderview'),
    # view order by staff
    path('orders_list/', views.orders_list, name='orders_list'),
    # new order by staff
    path('create_order/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    # invoice
    path('orders_pdf/', views.orders_pdf, name='orders_pdf'),
    
]