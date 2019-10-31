from django.db import models


DEVICE_ENVIRONMENT = [
    ('LAB', 'lab device'),
    ('PROD', 'production device'),
]


class Device(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    device = models.CharField(max_length=255)
    environment = models.CharField(max_length=4, choices=DEVICE_ENVIRONMENT, default='PROD')
    os_type = models.CharField(max_length=255)

    class Meta:
        ordering = ('id',)


class DeviceInterface(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    interface = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)


class InterfaceMapper(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    lab_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="lab")
    prod_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="prod")


class ConsoleServer(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    device = models.CharField(max_length=255)


class ConsolePort(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    console_device = models.ForeignKey(ConsoleServer, on_delete=models.CASCADE)
    console_port = models.IntegerField()
    client_device = models.ForeignKey(Device, on_delete=models.CASCADE)