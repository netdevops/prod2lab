from django.contrib import admin
from .models import Device
from .models import DeviceInterface
from .models import InterfaceMapper
from .models import ConsoleServer
from .models import ConsolePort


admin.site.register(Device)
admin.site.register(DeviceInterface)
admin.site.register(InterfaceMapper)
admin.site.register(ConsoleServer)
admin.site.register(ConsolePort)