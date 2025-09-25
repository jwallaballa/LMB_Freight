from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add_order_view, name='add_order'),
path('', views.dashboard_view, name='dashboard'),
]