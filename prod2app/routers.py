from rest_framework import routers
from lab.views import (
    DeviceViewSet,
    DevicePairViewSet,
    DeviceInterfaceViewSet,
    InterfaceMapperViewSet,
    RouteSwitchConfigViewSet,
)

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'pairs', DevicePairViewSet)
router.register(r'interfaces', DeviceInterfaceViewSet)
router.register(r'interface_mappings', InterfaceMapperViewSet)
router.register(r'configs', RouteSwitchConfigViewSet)
