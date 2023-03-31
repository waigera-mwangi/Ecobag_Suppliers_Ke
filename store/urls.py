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
    # path('order-list/', OrderListView.as_view(), name='order-list'),
    path('category_list/', category_list, name='category_list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
    # view products by customer
    path('view-products/', ProductView.as_view(), name='view-product'),
<<<<<<< HEAD
    path('product_detail/<slug:slug>/', product_detail, name='product_detail'),
    # path('category_view/<slug:category_slug>/', category_list, name='category_list'),
    # path('user/', userPage, name="user-page"),
=======
    # view single product by customer
    path('product_detail/<slug:name>/', views.product_detail, name='product_detail'),
    path('category_view/<slug:category_slug>/', views.category_list, name='category_list'),
    # path('user/', views.userPage, name="user-page"),
>>>>>>> 7f1a830933b5f41f8ac44e08e56091723d05a748

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
    # path('category-list/', CategoryListView.as_view(), name='category-list'),
    # path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    # path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    # path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete')
    


   
]
