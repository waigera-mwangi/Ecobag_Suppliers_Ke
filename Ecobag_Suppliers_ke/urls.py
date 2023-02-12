from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView

from accounts.decorators import required_access
from Ecobag_Suppliers_ke import settings
from django.contrib.auth import views as auth_views

# app_name = 'basket'
# app_name = 'payment'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', required_access(function=TemplateView.as_view(template_name="index.html"), login_url=reverse_lazy('accounts:login'), user_type="CM"), name="index"),
    path('', include('accounts.urls')),
    path('basket/', include('basket.urls', namespace = 'basket')),
    path('payment/', include('payment.urls', namespace = 'payment')),
    path('orders/', include('orders.urls', namespace = 'orders')),
    path('', include('store.urls')),
    path('', include('loans.urls')),

      # password reset urls
      path('reset_password/',
           auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
           name="reset_password"),

      path('reset_password_sent/',
           auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
           name="password_reset_done"),

      path('reset/<uidb64>/<token>/',
           auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
           name="password_reset_confirm"),

      path('reset_password_complete/',
           auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
           name="password_reset_complete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
