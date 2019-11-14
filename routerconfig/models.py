from django.db import models
from lab.models import Device


class RouteSwitchConfig(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return self.device.name
