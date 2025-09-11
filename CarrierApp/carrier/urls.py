from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrier_list, name='carrier_list'),
    path('add/', views.add_carrier, name='add_carrier'),
    path('<int:pk>/', views.carrier_detail, name='carrier_detail'),
]
