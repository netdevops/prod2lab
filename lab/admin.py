from django.contrib import admin
from lab.models import (
    Device,
    DevicePair,
    DeviceInterface,
    InterfaceMapper,
    RouteSwitchConfig,
    OperatingSystem,
    ConsoleServer,
    ConsolePort,
)


admin.site.register(Device)
admin.site.register(DevicePair)
admin.site.register(DeviceInterface)
admin.site.register(InterfaceMapper)
admin.site.register(RouteSwitchConfig)
admin.site.register(OperatingSystem)
admin.site.register(ConsoleServer)
admin.site.register(ConsolePort)
