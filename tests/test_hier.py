from django.test import TestCase
from hier.models import Lineage


class TestLineage(TestCase):

    def setUp(self):
        self.lineage1 = Lineage.objects.create(key='startswith', value='interface', os='iosxr')
        self.lineage2 = Lineage.objects.create(parent=self.lineage1, key='startswith', value='service-policy', os='iosxr')

    def test_lineage(self):
        self.assertEqual(self.lineage1.key, "startswith")
        self.assertEqual(self.lineage1.value, "interface")
        self.assertEqual(self.lineage1.os, "iosxr")
        self.assertEqual(self.lineage2.parent, self.lineage1)
        self.assertEqual(self.lineage2.key, "startswith")
        self.assertEqual(self.lineage2.value, "service-policy")
        self.assertEqual(self.lineage2.os, "iosxr")
        self.assertEqual(self.lineage1.__str__(), "iosxr: startswith:interface")
        self.assertEqual(self.lineage2.__str__(), "iosxr: startswith:interface > startswith:service-policy")
