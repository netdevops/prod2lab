from django.core import serializers
from hier.models import Lineage
import json


class HierSerializer:

    def __init__(self, os: str=None):
        self.os = os
        self.lineage = list()

        if self.os is None:
            self.data = json.loads(serializers.serialize("json", Lineage.objects.all()))
        else:
            self.data = json.loads(serializers.serialize("json", Lineage.objects.filter(os=self.os)))

    def fetch_lineage(self):
        for item in self.data:
            id = item['pk']

            if self._has_child(id=id) is False:
                if item['fields']['parent'] is None:
                    self.lineage.append(
                        {"lineage": [{f"{item['fields']['key']}": [f"{item['fields']['value']}"]}], "add_tags": "ignore"}
                    )
                else:
                    parent = Lineage.objects.get(id=item['fields']['parent'])

                    self.lineage.append(
                        {"lineage": [
                            {f"{parent.key}": [f"{parent.value}"]},
                            {f"{item['fields']['key']}": [f"{item['fields']['value']}"]}
                        ], "add_tags": "ignore"}
                    )

        return self.lineage

    def add_lineage(self, rule: dict=None):
        return self.lineage.append(rule)

    def _has_child(self, id=None):
        child_exists = False
        for item in self.data:
            if item['fields']['parent']:
                if id == item['fields']['parent']:
                    child_exists = True

        return child_exists
