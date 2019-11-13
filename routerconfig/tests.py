from django.test import TestCase
from routerconfig.models import RouteSwitchConfig
from lab.models import Device
from datetime import datetime


class RouteSwitchConfigTestCase(TestCase):

    def setUp(self):
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

    def test_config_storage(self):
        device_config = RouteSwitchConfig.objects.create(device=self.device, text=self.config_text, created=datetime.now())
        self.assertEquals(device_config.text, self.config_text)