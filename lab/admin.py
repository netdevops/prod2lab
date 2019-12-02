from django.contrib import admin
from lab.models import Device
from lab.models import DevicePair
from lab.models import DeviceInterface
from lab.models import InterfaceMapper
from lab.models import RouteSwitchConfig
from lab.models import OperatingSystem


admin.site.register(Device)
admin.site.register(DevicePair)
admin.site.register(DeviceInterface)
admin.site.register(InterfaceMapper)
admin.site.register(RouteSwitchConfig)
admin.site.register(OperatingSystem)
