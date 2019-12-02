from django.db import models


DEVICE_ENVIRONMENT = [
    ('LAB', 'lab device'),
    ('PROD', 'production device'),
]


class ConsoleServer(models.Model):
    name = models.CharField(max_length=255)
    port_prefix = models.IntegerField()

    def __str__(self):
        return self.name


class ConsolePort(models.Model):
    device = models.ForeignKey(ConsoleServer, on_delete=models.CASCADE)
    port = models.IntegerField()

    def __str__(self):
        return f"{self.device.name}: {self.port}"


class OperatingSystem(models.Model):
    name = models.CharField(max_length=255)
    netmiko_type = models.CharField(max_length=255)
    terminal_length_cmd = models.CharField(max_length=255)
    fetch_config_cmd = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=255, blank=False)
    environment = models.CharField(max_length=4, choices=DEVICE_ENVIRONMENT, default='PROD')
    os_type = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE)
    console = models.ForeignKey(ConsolePort, on_delete=models.CASCADE, blank=True, null=True, related_name="console")

    def __str__(self):
        return f"{self.name} - {self.environment}"


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


class InterfaceMapper(models.Model):
    lab_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="lab")
    prod_device = models.ForeignKey(DeviceInterface, on_delete=models.CASCADE, related_name="prod")

    def __str__(self):
        return f"{self.prod_device.device.name}:{self.prod_device.name} > {self.lab_device.device.name}:{self.lab_device.name}"


class RouteSwitchConfig(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return self.device.name
