from django.urls import path

from .views import (
    Apply_loan

)

urlpatterns = [
    path('loan-application/', Apply_loan, name='loan-application'),
]
