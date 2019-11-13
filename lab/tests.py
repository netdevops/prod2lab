from django.test import TestCase
from .models import Device
from .models import DeviceInterface
from .models import InterfaceMapper


class DeviceMapperTestCase(TestCase):

    def setUp(self):
        self.prod_device = Device.objects.create(name="pe1.dc1", environment="PROD", os_type="iosxr")
        self.prod_interface = DeviceInterface.objects.create(device=self.prod_device, name="tengige0/0/0/0")
        self.lab_device = Device.objects.create(name="pe1.dc1-lab", environment="LAB", os_type="iosxr")
        self.lab_interface = DeviceInterface.objects.create(device=self.lab_device, name="gig0/0/0/0")
        self.interface_mapper = InterfaceMapper.objects.create(lab_device=self.lab_interface, prod_device=self.prod_interface)

    def test_device_creation(self):
        self.assertEquals(self.prod_device.name, "pe1.dc1")
        self.assertEquals(self.prod_device.environment, "PROD")
        self.assertEquals(self.prod_device.os_type, "iosxr")
        self.assertEquals(self.lab_device.name, "pe1.dc1-lab")
        self.assertEquals(self.lab_device.environment, "LAB")
        self.assertEquals(self.lab_device.os_type, "iosxr")

    def test_interface_creation(self):
        self.assertEquals(self.lab_interface.name, "gig0/0/0/0")
        self.assertEquals(self.lab_interface.device, self.lab_device)
        self.assertEquals(self.prod_interface.name, "tengige0/0/0/0")
        self.assertEquals(self.prod_interface.device, self.prod_device)

    def test_interface_mapper(self):
        self.assertEquals(self.interface_mapper.lab_device, self.lab_interface)
        self.assertEquals(self.interface_mapper.prod_device, self.prod_interface)