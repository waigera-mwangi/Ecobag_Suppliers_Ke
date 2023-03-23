from store import views

from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    path('SM-dashboard', views.SM_dashboard, name='SM-dashboard'),

    # path('create-buyer/', create_buyer, name='create-buyer'),
    # path('create-drop/', create_drop, name='create-drop'),
    path('invoice/', invoice, name='invoice'),
    

    # path('customer-list/', CustomerListView.as_view(), name='customer-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    # path('order-list/', OrderListView.as_view(), name='order-list'),
    path('category_list/', views.category_list, name='category_list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
    path('view-products/', view_product, name='view-product'),
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category_view/<slug:category_slug>/', views.category_list, name='category_list'),
    # path('user/', views.userPage, name="user-page"),

    path('products/', product, name='products'),
    # search products
    path('product-search-list/', views.productlistAjax, name='product-search-list'),
    path('searchproduct', views.searchproduct, name='searchproduct'),
   
#    update stock by inventory
    path('create_category/', views.create_category, name='create_category'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_category/<str:pk>/', views.update_category, name='update_category'),
    path('update_product/<str:pk>/', views.update_product, name='update_product'),
    path('delete_category/<str:pk>/', views.delete_category, name='delete_category'),
    path('delete_product/<str:pk>/', views.delete_product, name='delete_product'),
    


   
]
