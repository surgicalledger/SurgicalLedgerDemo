from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('scan/', views.scan, name='scan'),
    path('scan-log/', views.scan_log, name='scan_log'),
]
