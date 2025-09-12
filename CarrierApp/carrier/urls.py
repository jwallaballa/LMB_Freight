# carrier/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrier_list, name='carrier_list'),
    path('add/', views.add_carrier, name='add_carrier'),
    path('<int:pk>/', views.carrier_detail, name='carrier_detail'),
    path('<int:pk>/edit/', views.edit_carrier, name='edit_carrier'),
    path('update-field/<int:pk>/', views.update_carrier_field, name='update_carrier_field'),
    path('update-rate/<int:pk>/', views.update_carrier_rate, name='update_carrier_rate'),
]