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
    path('inventory/', inventory, name='inventory'),
    path('manager/', manager, name='manager'),
    path('brander/', brander, name='brander'),
    path('dispatch-manager/', views.dispatch_manager, name='dispatch-manager'),
    path('finance-manager/', views.finance_manager, name='finance-manager'),
    path('driver/', views.driver, name='driver'),
    path('supplier/', views.supplier, name='supplier'),
    # path('profile', views.profile, name='customer'),
    path('change-password', password_change, name='change-password'),
    # path('profile', views.profile, name='profile'),
    # path('supplier/', required_access(function=TemplateView.as_view(template_name="Supplier.html"),
                                #    login_url=reverse_lazy('accounts:Supplier-login'), user_type="RD"), name="index"),


    # faqs
    path('customer-faq/', FAQQuestionTypeListView.as_view(), name='faq_question_types'),
    path('driver-faq/', D_FAQ.as_view(), name='driver-faq'),
    path('supplier-faq/', S_FAQ.as_view(), name='supplier-faq'),
    path('brander-faq/', B_FAQ.as_view(), name='brander-faq'),
    path('inventory-faq/', I_FAQ.as_view(), name='inventory-faq'),
    path('dispatch-faq/', DP_FAQ.as_view(), name='dispatch-faq'),
    path('finance-faq/', F_FAQ.as_view(), name='finance-faq'),
    

    # profile
    path('customer-profile', customer_profile, name='customer-profile'),
    path('finance-profile', finance_profile, name='finance-profile'),
    path('brander-profile', brander_profile, name='brander-profile'),
    path('dispatch-profile', dispatch_profile, name='dispatch-profile'),
    path('driver-profile', driver_profile, name='driver-profile'),
    path('inventory-profile', inventory_profile, name='inventory-profile'),
    path('supplier-profile', supplier_profile, name='supplier-profile'),

    # change password
    path('customer/password-change', customer_password_change, name='customer_password_change'),
    path('supplier/password-change', supplier_password_change, name='supplier_password_change'),
    path('inventory/password-change', inventory_password_change, name='inventory_password_change'),
    path('dispatch/password-change', dispatch_password_change, name='dispatch_password_change'),
    path('brander/password-change', brander_password_change, name='brander_password_change'),
    path('driver/password-change', driver_password_change, name='driver_password_change'),
    path('finance/password-change', finance_password_change, name='finance_password_change'),


     # password reset urls
      path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
           name="password_reset"),

      path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
           name="password_reset_done"),

      path('reset_password_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
           name="password_reset_confirm"),

      path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html.html"),
           name="password_reset_complete"),
]
