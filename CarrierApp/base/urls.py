
from django.urls import path, include
from django.contrib import admin


import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('orders/', include('order.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('carriers/', include('carrier.urls')),

]
