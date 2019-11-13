from django.db import models


DEVICE_ENVIRONMENT = [
    ('LAB', 'lab device'),
    ('PROD', 'production device'),
]


class Device(models.Model):
    name = models.CharField(max_length=255, blank=False)
    environment = models.CharField(max_length=4, choices=DEVICE_ENVIRONMENT, default='PROD')
    os_type = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ('id',)


class DevicePair(models.Model):
    prod_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="prod")
    lab_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="lab")


class DeviceInterface(models.Model):
    name = models.CharField(max_length=255, blank=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)


class InterfaceMapper(models.Model):
    lab_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="lab")
    prod_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="prod")