from django.urls import path
from .views import *

app_name = 'shipping'


urlpatterns = [

		path('select-pickup-station', UserPickUpStationCreateView.as_view(), name='select-pickup-station')

]