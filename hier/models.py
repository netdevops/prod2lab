from django.db import models


LINEAGE_CHOICES = (
    ('startswith', 'startswith'),
    ('endswith', 'endswith'),
    ('contains', 'contains'),
    ('equals', 'equals')
)


class Lineage(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    key = models.CharField(choices=LINEAGE_CHOICES, blank=False, null=False, max_length=255)
    value = models.CharField(max_length=500, blank=False, null=False)
    os = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        if self.parent:
            return f"{self.os}: {self.parent.key}:{self.parent.value} > {self.key}:{self.value}"
        else:
            return f"{self.os}: {self.key}:{self.value}"
