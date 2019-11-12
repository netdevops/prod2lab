from django.urls import path
from . import views

urlpatterns = [
    path('', views.devices, name='devices'),
    path('devices/', views.devices, name='devices'),
    path('devices/add/', views.device_add, name='add_device'),
    path('devices/<int:device_id>/', views.device, name='device'),
    path('devices/<int:device_id>/modify/', views.device, name='modify_device'),
    path('devices/<int:device_id>/delete/', views.device_delete, name='delete_device'),
    path('devices/<int:device_id>/interface/add/', views.interface_add, name='add_interface'),
    path('devices/<int:device_id>/interface/<int:interface_id>/delete/', views.interface_delete, name='delete_interface'),
    path('devices/<int:device_id>/interface_mapper/add/', views.interface_mapper_add, name='add_interface_mapper'),
]