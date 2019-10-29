from django.test import TestCase
from .models import Device
from .models import DeviceInterface
from .models import InterfaceMapper
from .models import ConsoleServer
from .models import ConsolePort


class DeviceMapperTestCase(TestCase):

    def setUp(self):
        self.prod_device = Device.objects.create(device="pe1.dc1", environment="prod")
        self.prod_interface = DeviceInterface.objects.create(device=self.prod_device, interface="tengige0/0/0/0")
        self.lab_device = Device.objects.create(device="pe1.dc1-lab", environment="lab")
        self.lab_interface = DeviceInterface.objects.create(device=self.lab_device, interface="gig0/0/0/0")
        self.interface_mapper = InterfaceMapper.objects.create(lab_device=self.lab_interface, prod_device=self.prod_interface)
        self.console_server = ConsoleServer.objects.create(device="oob-router.dc1")
        self.console_port = ConsolePort.objects.create(console_device=self.console_server, console_port=2001, client_device=self.lab_device)

    def test_device_creation(self):
        self.assertEquals(self.prod_device.environment, "prod")
        self.assertEquals(self.lab_device.environment, "lab")

    def test_interface_creation(self):
        self.assertEquals(self.lab_interface.interface, "gig0/0/0/0")
        self.assertEquals(self.lab_interface.device, self.lab_device)
        self.assertEquals(self.prod_interface.interface, "tengige0/0/0/0")
        self.assertEquals(self.prod_interface.device, self.prod_device)

    def test_interface_mapper(self):
        self.assertEquals(self.interface_mapper.lab_device, self.lab_interface)
        self.assertEquals(self.interface_mapper.prod_device, self.prod_interface)

    def test_console_server_creation(self):
        self.assertEquals(self.console_server.device, "oob-router.dc1")
    
    def test_console_port_creation(self):
        self.assertEquals(self.console_port.console_device, self.console_server)
        self.assertEquals(self.console_port.console_port, 2001)
        self.assertEquals(self.console_port.client_device, self.lab_device)