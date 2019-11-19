from django.contrib import admin
from .models import Device
from .models import DevicePair
from .models import DeviceInterface
from .models import InterfaceMapper
from .models import RouteSwitchConfig


admin.site.register(Device)
admin.site.register(DevicePair)
admin.site.register(DeviceInterface)
admin.site.register(InterfaceMapper)
admin.site.register(RouteSwitchConfig)
