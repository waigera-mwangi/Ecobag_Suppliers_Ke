from store import views

from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    path('SM-dashboard', SM_dashboard, name='SM-dashboard'),

    # path('create-buyer/', create_buyer, name='create-buyer'),
    # path('create-drop/', create_drop, name='create-drop'),
    path('invoice/', invoice, name='invoice'),
    

    # path('customer-list/', CustomerListView.as_view(), name='customer-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    # path('order-list/', OrderListView.asdelete_c_view(), name='order-list'),
   

    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
    # view products by customer
    path('view-products/', ProductView.as_view(), name='view-product'),
    path('product_detail/<slug:name>/', product_detail, name='product_detail'),
    path('update_category/<str:pk>/', views.update_category, name='update_category'),
    path('inventory_category_list/', views.inventory_category_list, name='inventory_category_list'),
    path('create_category/', views.create_category, name='create_category'),
    
    
    # view single product by customer
    path('product_detail/<slug:name>/', views.product_detail, name='product_detail'),

    path('products/', product, name='products'),
    # search products
    path('product-search-list/', productlistAjax, name='product-search-list'),
    path('searchproduct', searchproduct, name='searchproduct'),
   
#    update stock by inventory
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-detail/<int:pk>/', ProductDetailViewCustomer.as_view(), name='product-detail-customer'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
     # finance
    path('approve-payment/<str:transaction_id>/', approve_payment, name='approve_payment'),
    path('order-payments/', order_payment, name='order-payment'),
    path('order/approved-payments/', order_approved_payment, name='order-payment-approved'),
    path('order/rejected-payments/', order_rejected_payment, name='order-payment-rejected'),


    # organised
    path('customer-order-list/', customer_order_list, name='customer-order-list'),
    path('customer-order-details/<int:order_id>/', customer_order_detail, name='customer-order-details'),
    path('customer-invoice/', customer_order_invoice, name='customer-invoice'),
    path('order/<int:order_id>/pdf/', views.customer_order_pdf, name='customer-order-pdf'),

#    customer
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),

    # dispatch
    path('assign-order-list/', assign_driver_order_list, name='assign-order-list'),
    path('assigned-order-list/', assigned_order_list, name='assigned-order-list'),


     #  view product by categories
    path('category_view/<slug:category_slug>/', views.category_list, name='category_list'),
     path('category/<slug:slug>/', ProductByCategoryView.as_view(), name='product_by_category'),

]
