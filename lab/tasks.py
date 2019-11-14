from celery import shared_task
from netmiko import Netmiko
from datetime import datetime
from .models import Device
from .models import RouteSwitchConfig


@shared_task
def fetch_production_config(device_id, username, password, command):
    device = Device.objects.get(id=device_id)
    host = {
        "host": device.name,
        "username": username,
        "password": password,
        "device_type": device.os_type
    }
    nm = Netmiko(**host)
    nm.send_command("terminal length 0")
    result = nm.send_command(command)

    try:
        RouteSwitchConfig.objects.get(device=device)
        RouteSwitchConfig.objects.update(device=device, text=result)
    except RouteSwitchConfig.DoesNotExist:
        RouteSwitchConfig.objects.create(device=device, text=result, created=datetime.now())

    return result