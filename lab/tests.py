from django.test import TestCase
from .models import Device
from .models import DevicePair
from .models import DeviceInterface
from .models import InterfaceMapper
from .models import RouteSwitchConfig
from datetime import datetime


class DeviceMapperTestCase(TestCase):

    def setUp(self):
        self.prod_device = Device.objects.create(name="pe1.dc1", environment="PROD", os_type="iosxr")
        self.prod_interface = DeviceInterface.objects.create(device=self.prod_device, name="tengige0/0/0/0")
        self.lab_device = Device.objects.create(name="pe1.dc1-lab", environment="LAB", os_type="iosxr")
        self.lab_interface = DeviceInterface.objects.create(device=self.lab_device, name="gig0/0/0/0")
        self.device_pair = DevicePair.objects.create(prod_device=self.prod_device, lab_device=self.lab_device)
        self.interface_mapper = InterfaceMapper.objects.create(lab_device=self.lab_interface, prod_device=self.prod_interface)
        self.device = Device.objects.create(name='router.dc1', environment='PROD', os_type='iosxr')
        self.config_text = """hostname router1.dc1
        !
        interface gige0/0/0/1
         ipv4 address 10.0.0.0/31
         no shutdown
        !
        interface gige0/0/0/2
         ipv4 address 10.0.0.2/31
         no shutdown
        """

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

    def test_device_pair(self):
        self.assertEquals(self.device_pair.prod_device, self.prod_device)
        self.assertEquals(self.device_pair.lab_device, self.lab_device)

    def test_config_storage(self):
        device_config = RouteSwitchConfig.objects.create(device=self.device, text=self.config_text, created=datetime.now())
        self.assertEquals(device_config.text, self.config_text)