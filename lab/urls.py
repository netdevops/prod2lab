from django.urls import path
from lab import views

urlpatterns = [
    path('', views.devices, name='devices'),
    path('devices/', views.devices, name='devices'),
    path('devices/add/', views.device_add, name='add_device'),
    path('devices/<int:device_id>/', views.device, name='device'),
    path('devices/<int:device_id>/modify/', views.device, name='modify_device'),
    path('devices/<int:device_id>/delete/', views.device_delete, name='delete_device'),
    path('devices/<int:device_id>/interface/add/', views.interface_add, name='add_interface'),
    path('devices/<int:device_id>/interface/fetch/', views.interface_fetch, name='fetch_interfaces'),
    path('devices/<int:device_id>/interface/<int:interface_id>/delete/', views.interface_delete, name='delete_interface'),
    path('devices/<int:device_id>/interface_mapper/add/', views.interface_mapper_add, name='add_interface_mapper'),
    path('devices/<int:device_id>/interface_mapper/<int:interface_mapper_id>/delete/',
         views.interface_mapper_delete, name='delete_interface_map'),
    path('devices/<int:device_id>/config/update/', views.device_config, name='fetch_device_config'),
    path('devices/<int:device_id>/config/update/manually/', views.device_config_manually, name='manually_fetch_device_config'),
    path('console_servers/', views.consoles, name="console_servers"),
    path('console_servers/add/', views.console_add, name="add_console"),
    path('console_servers/ports/<int:port_id>/add_attachment/', views.attachment_add, name="add_attachment"),
    path('console_servers/ports/<int:port_id>/remove_attachment/', views.attachment_remove, name="remove_attachment"),
    path('console_servers/<int:console_id>/', views.console, name="console_server"),
    path('console_servers/<int:console_id>/delete/', views.console_delete, name="delete_console"),
]
