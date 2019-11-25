from django import forms
from hier.models import (
    Lineage,
)


class AddLineageForm(forms.Form):
    class Meta:
        model = Lineage
        fields = ['parent', 'key', 'value', 'os']
