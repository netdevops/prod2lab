from celery import shared_task
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result
from netmiko import Netmiko
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
    logging={
        "level": "debug"
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
def fetch_production_config(device, username, password, device_type, command="show running-configuration"):
    # nr.inventory.hosts[f"{device}.prod"].username = username
    # nr.inventory.hosts[f"{device}.prod"].password = password
    # host = nr.filter(groups=["PROD"], hostname=device)
    # host.run(task=networking.netmiko_send_command, command_string="terminal length 0")
    # result = host.run(task=networking.netmiko_send_command, command_string="show configuration")
    # print_result(result, vars=["stdout"])

    # return print_result(result, vars=["stdout"])

    host = {
        "host": device,
        "username": username,
        "password": password,
        "device_type": device_type
    }
    nm = Netmiko(**host)
    nm.send_command("terminal length 0")
    result = nm.send_command(command)

    return result