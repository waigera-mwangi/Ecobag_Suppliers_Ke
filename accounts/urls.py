from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from accounts import views
from accounts.decorators import required_access
from accounts.views import *

app_name = "accounts"

urlpatterns = [
    path('register/', UserCreateView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # staff urls
    path('', views.loginView, name='login'),
    path('customer/', views.customer, name='customer'),
    path('inventory-manager/', views.inventory_manager, name='inventory-manager'),
    path('manager/', views.manager, name='manager'),
    path('brander/', views.brander, name='brander'),
    path('dispatch-manager/', views.dispatch_manager, name='dispatch-manager'),
    path('finance-manager/', views.finance_manager, name='finance-manager'),
    path('driver/', views.driver, name='driver'),
    path('supplier/', views.supplier, name='supplier'),
    # path('profile', views.profile, name='customer'),
    path('change-password', password_change, name='change-password'),
    path('profile', views.profile, name='profile'),
    # path('supplier/', required_access(function=TemplateView.as_view(template_name="Supplier.html"),
                                #    login_url=reverse_lazy('accounts:Supplier-login'), user_type="RD"), name="index"),
]
