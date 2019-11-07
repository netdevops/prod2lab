from django.urls import path
from . import views

urlpatterns = [
    path('', views.devices, name='devices'),
    path('devices/', views.devices, name='devices'),
    path('devices/add/', views.device_add, name='add_device'),
    path('devices/<int:id>/', views.device, name='device'),
    path('devices/<int:id>/modify/', views.device, name='modify_device'),
    path('devices/<int:id>/delete/', views.device_delete, name='delete_device'),
    path('devices/<int:id>/interface/add/', views.interface_add, name='add_interface'),
    path('devices/<int:id>/interface/modify/', views.interface_modify, name='modify_interface'),
    path('devices/<int:id>/interface/delete/', views.interface_delete, name='delete_interface'),
    path('console_servers/', views.console_servers, name='console_servers'),
    path('console_servers/add/', views.console_servers_add, name='add_console_server'),
    path('console_servers/modify/', views.console_servers_modify, name='modify_console_server'),
    path('console_servers/delete/', views.console_servers_delete, name='delete_console_server'),
    path('console_servers/<int:id>/', views.console_servers, name='console_server'),
    path('console_servers/<int:id>/port/add/', views.console_port_add, name='add_console_port'),
    path('console_servers/<int:id>/port/modify/', views.console_port_modify, name='modify_console_port'),
    path('console_servers/<int:id>/port/delete/', views.console_port_delete, name='delete_console_port'),
]