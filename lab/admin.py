from django.contrib import admin
from .models import Device
from .models import DeviceInterface
from .models import InterfaceMapper


admin.site.register(Device)
admin.site.register(DeviceInterface)
admin.site.register(InterfaceMapper)