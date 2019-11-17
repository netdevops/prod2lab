from django.test import TestCase
from lab.models import Device
from lab.models import DevicePair
from lab.models import DeviceInterface
from lab.models import InterfaceMapper
from lab.models import RouteSwitchConfig


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
        self.assertEqual(self.prod_device.name, "pe1.dc1")
        self.assertEqual(self.prod_device.environment, "PROD")
        self.assertEqual(self.prod_device.os_type, "iosxr")
        self.assertEqual(self.lab_device.name, "pe1.dc1-lab")
        self.assertEqual(self.lab_device.environment, "LAB")
        self.assertEqual(self.lab_device.os_type, "iosxr")
        self.assertEqual(self.prod_device.__str__(), "pe1.dc1 - PROD")

    def test_interface_creation(self):
        self.assertEqual(self.lab_interface.name, "gig0/0/0/0")
        self.assertEqual(self.lab_interface.device, self.lab_device)
        self.assertEqual(self.prod_interface.name, "tengige0/0/0/0")
        self.assertEqual(self.prod_interface.device, self.prod_device)
        self.assertEqual(self.prod_interface.__str__(), "pe1.dc1 - tengige0/0/0/0")

    def test_interface_mapper(self):
        self.assertEqual(self.interface_mapper.lab_device, self.lab_interface)
        self.assertEqual(self.interface_mapper.prod_device, self.prod_interface)
        self.assertEqual(self.interface_mapper.__str__(), "pe1.dc1:tengige0/0/0/0 > pe1.dc1-lab:gig0/0/0/0")

    def test_device_pair(self):
        self.assertEqual(self.device_pair.prod_device, self.prod_device)
        self.assertEqual(self.device_pair.lab_device, self.lab_device)
        self.assertEqual(self.device_pair.__str__(), "pe1.dc1")

    def test_config_storage(self):
        device_config = RouteSwitchConfig.objects.create(device=self.device, text=self.config_text)
        self.assertEqual(device_config.text, self.config_text)
        self.assertEqual(device_config.__str__(), "router.dc1")
