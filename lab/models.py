from django.db import models


DEVICE_ENVIRONMENT = [
    ('LAB', 'lab device'),
    ('PROD', 'production device'),
]


class Device(models.Model):
    device = models.CharField(max_length=255)
    environment = models.CharField(max_length=4, choices=DEVICE_ENVIRONMENT, default='PROD')
    os_type = models.CharField(max_length=255)

    class Meta:
        ordering = ('device', 'environment', 'os_type')

    def __str__(self):
        return f"{self.device}: {self.environment}"


class DeviceInterface(models.Model):
    interface = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        ordering = ('device', 'interface')
    
    def __str__(self):
        return f"{self.device}: {self.interface}"


class InterfaceMapper(models.Model):
    lab_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="lab")
    prod_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="prod")

    def __str__(self):
        return f"{self.prod_device} -> {self.lab_device}"


class ConsoleServer(models.Model):
    device = models.CharField(max_length=255)

    def __str__(self):
        return self.device


class ConsolePort(models.Model):
    console_device = models.ForeignKey(ConsoleServer, on_delete=models.CASCADE)
    console_port = models.IntegerField()
    client_device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.console_device}: {self.console_port} -> {self.client_device}"