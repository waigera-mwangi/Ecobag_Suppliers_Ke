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
    path('', include('accounts.urls')),
    path('basket/', include('basket.urls', namespace = 'basket')),
    # path('orders/', include('orders.urls', namespace = 'orders')),
    path('', include('store.urls')),
    path('', include('brands.urls')),
    path('', include('supply.urls')),
    path('shipping/', include('shipping.urls')),
    path('finance/', include('finance.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
