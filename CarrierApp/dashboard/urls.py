from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('update-order/', views.update_order_view, name='update_order'),
]
