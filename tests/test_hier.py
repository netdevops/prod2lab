from django.test import TestCase
from hier.models import Lineage
from hier.serializers import HierSerializer


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

    def test_serializer(self):
        self.lineage_serializer = HierSerializer(os='iosxr')
        self.lineage_serializer.add_lineage({"lineage": [self.lineage1, self.lineage2]})
        self.assertTrue(isinstance(self.lineage_serializer.fetch_lineage(), list))
        self.assertEqual(self.lineage_serializer.os, "iosxr")
        self.assertTrue(self.lineage_serializer._has_child(id=self.lineage1.id))
        self.assertFalse(self.lineage_serializer._has_child(id=self.lineage2.id))
