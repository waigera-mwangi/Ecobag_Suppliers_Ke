from django.urls import path
from . import views
from .views import *

app_name = 'finance'


urlpatterns = [
			path('checkout/', views.checkout, name='checkout')
		
]
