from celery import shared_task
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result
from lab.models import Device
from lab.models import DeviceInterface


all_devices = Device.objects.all()
devices = dict()

for device in all_devices:
    interface_objs = DeviceInterface.objects.filter(device=device)
    interfaces = [interface.name for interface in interface_objs]
    devices[f"{device.name}.{device.environment.lower()}"] = {
        "hostname": device.name,
        "username": str(),
        "password": str(),
        "platform": device.os_type,
        "port": 22,
        "groups": [device.environment],
        "data": {
            "interfaces": interfaces
        }
    }

nr = InitNornir(
    core={
        "num_workers": 50,
    },
    ssh={
        "config_file": "~/.ssh/config"
    },
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "hosts": devices,
            "groups": {
                "PROD": {},
                "LAB": {},
            }
        }
    }
)

@shared_task
def fetch_production_config(device, username, password):
    nr.inventory.hosts[f"{device}.prod"].username = username
    nr.inventory.hosts[f"{device}.prod"].password = password
    host = nr.filter(groups=["PROD"], hostname=device)
    result = host.run(task=networking.netmiko_send_command, command_string="show running-config")
    print_result(result)

    return print_result(result)