from django.db import models


DEVICE_ENVIRONMENT = [
    ('LAB', 'lab device'),
    ('PROD', 'production device'),
]


class Device(models.Model):
    name = models.CharField(max_length=255, blank=False)
    environment = models.CharField(max_length=4, choices=DEVICE_ENVIRONMENT, default='PROD')
    os_type = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.name} - {self.environment}"

    class Meta:
        ordering = ('id',)


class DevicePair(models.Model):
    prod_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="prod")
    lab_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="lab")

    def __str__(self):
        return self.prod_device.name


class DeviceInterface(models.Model):
    name = models.CharField(max_length=255, blank=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device.name} - {self.name}"

    class Meta:
        ordering = ('id',)


class InterfaceMapper(models.Model):
    lab_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="lab")
    prod_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="prod")

    def __str__(self):
        return f"{self.prod_device.device.name}:{self.prod_device.name} > {self.lab_device.device.name}:{self.lab_device.name}"


class RouteSwitchConfig(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return self.device.name
