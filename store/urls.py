from store import views

from django.urls import path

from .views import (
    create_product,
    create_delivery,
    ProductListView,
    OrderListView,
    DeliveryListView,
    invoice,
    view_product, product_detail, product, customer, updateOrder, deleteOrder, add_to_cart, cart_list, order_list, checkout_pay,
    checkout, clear_cart, increase_quantity, decrease_quantity, remove_from_cart,
)

app_name = "store"

urlpatterns = [
    path('SM-dashboard', views.SM_dashboard, name='SM-dashboard'),

    # path('create-buyer/', create_buyer, name='create-buyer'),
    # path('create-drop/', create_drop, name='create-drop'),
    path('add-product/', create_product, name='add-product'),
    path('invoice/', invoice, name='invoice'),
    path('create-delivery/', create_delivery, name='create-delivery'),

    # path('customer-list/', CustomerListView.as_view(), name='customer-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
    path('view-products/', view_product, name='view-product'),
    path('product_detail/', product_detail, name='product_detail'),
    path('user/', views.userPage, name="user-page"),

    path('products/', product, name='products'),
    path('customer/<str:pk_test>/', customer, name="customer"),

    path('update_order/<str:pk>/', updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', deleteOrder, name="delete_order"),



    # cart
    path('order_list/', order_list, name="order_list"),
    path('checkout_pay/', checkout_pay, name="checkout_pay"),
    path('checkout/', checkout, name="checkout"),
    path('clear_cart/', clear_cart, name="clear_cart"),
    path('increase_quantity/<slug>/', increase_quantity, name="increase_quantity"),
    path('decrease_quantity/<slug>/', decrease_quantity, name="decrease_quantity"),
    path('remove_from_cart/<slug>/', remove_from_cart, name="remove_from_cart"),
    path('cart_list/', cart_list, name="cart_list"),
    path('add_to_cart/', add_to_cart, name="add_to_cart"),
    # path('order_list/', customer_required(views.OrderListView.as_view()), name="order_list"),
]
