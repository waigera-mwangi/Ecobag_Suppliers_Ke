from django.urls import path, include, reverse_lazy

from . import views

app_name = 'basket'

urlpatterns = [
    path('',views.basket_summary, name ='basket_summary'),
    path('add/', views.basket_add, name = 'basket_add'),
    path('delete/', views.basket_delete, name = 'basket_delete')
]