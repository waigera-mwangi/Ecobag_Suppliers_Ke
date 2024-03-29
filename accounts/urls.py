from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from accounts import views
from accounts.decorators import required_access
from accounts.views import *
from accounts.views import CustomPasswordResetView, CustomPasswordResetDoneView,CustomPasswordResetConfirmView,CustomPasswordResetCompleteView

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
    path('about-us/', about_us, name='about-us'),
    

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
      path('reset_password/', CustomPasswordResetView.as_view(), name="password_reset"),
     #  path('reset_password/', auth_views.PasswordResetView.as_view(), name="password_reset"),

      path('reset_password_done/', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
     #  path('reset_password_done/',auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

      path('reset_password_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),name="password_reset_confirm"),
     #  path('reset_password_confirm/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

      path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
     #  path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
     
    #  feedback urls
    path('customer/view/feedback/', customer_feedback_view, name='customer_feedback'),
    path('finance/view/feedback/', finance_feedback_view, name='finance_feedback'),
    path('inventory/view/feedback/', inventory_feedback_view, name='inventory_feedback'),
    path('brander/view/feedback/', brander_feedback_view, name='brander_feedback'),
    path('supplier/view/feedback/', supplier_feedback_view, name='supplier_feedback'),
    path('dispatch/view/feedback/', dispatch_feedback_view, name='dispatch_feedback'),
    path('driver/view/feedback/', driver_feedback_view, name='driver_feedback'),
    
    # send feedback urls
    path('feedback/customer/send/', customer_send_feedback_view, name='customer_send_feedback'),
    path('feedback/finance/send/', finance_send_feedback_view, name='finance_send_feedback'),
    path('feedback/inventory/send/', inventory_send_feedback_view, name='inventory_send_feedback'),
    path('feedback/brander/send/', brander_send_feedback_view, name='brander_send_feedback'),
    path('feedback/supplier/send/', supplier_send_feedback_view, name='supplier_send_feedback'),
    path('feedback/dispatch/send/', dispatch_send_feedback_view, name='dispatch_send_feedback'),
    path('feedback/driver/send/', driver_send_feedback_view, name='driver_send_feedback'),

]
