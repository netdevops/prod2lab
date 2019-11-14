from celery import shared_task
from netmiko import Netmiko
from datetime import datetime
from hier_config.host import Host
from .models import Device
from .models import DevicePair
from .models import DeviceInterface
from .models import RouteSwitchConfig
from .models import InterfaceMapper


@shared_task
def fetch_production_config(device_id, username, password, command):
    device = Device.objects.get(id=device_id)
    platform_mapper = {
        "junos": "juniper_junos",
        "iosxr": "cisco_xr",
        "iosxe": "cisco_xe",
        "nxos": "cisco_nxos",
        "ios": "cisco_ios",
        "eos": "arista_eos",
    }

    host = {
        "host": device.name,
        "username": username,
        "password": password,
        "device_type": platform_mapper[device.os_type]
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


@shared_task
def fetch_lab_config(device_id):
    device = Device.objects.get(id=device_id)
    device_pair = DevicePair.objects.get(lab_device=device)
    other_device = device_pair.prod_device
    interfaces = DeviceInterface.objects.filter(device=device)
    interface_maps = list()

    for interface in interfaces:
        interface_maps.append(
            InterfaceMapper.objects.get(lab_device=interface)
        )

    interface_replace_maps = list()

    for item in interface_maps:
        interface_replace_maps.append(
            {"search": item.prod_device.name, "replace": item.lab_device.name }
        )

    options = {
        "style": device.os_type,
        "sectional_overwrite": [],
        "sectional_overwrite_no_negate": [],
        "indent_adjust": [],
        "parent_allows_duplicate_child": [],
        "sectional_exiting": [],
        "full_text_sub": [
            { "search": "^aaa", "replace": ""},
            { "search": "^tacacs", "replace": ""},
            { "search": "^logging", "replace": ""},
            { "search": "^ntp", "replace": ""},
        ],
        "per_line_sub": interface_replace_maps,
        "idempotent_commands_blacklist": [],
        "idempotent_commands": [],
        "negation_default_when": [],
        "negation_negate_with": [],
    }

    prod_config = RouteSwitchConfig.objects.get(id=other_device.id)
    host = Host(device.name, os=device.os_type, hconfig_options=options)
    host.load_config_from(name=prod_config.text, config_type="running", load_file=False)
    result = str()

    for line in host.running_config.all_children():
        result += line.cisco_style_text()
        result += "\n"

    try:
        RouteSwitchConfig.objects.get(device=device)
        RouteSwitchConfig.objects.update(device=device, text=result)
    except RouteSwitchConfig.DoesNotExist:
        RouteSwitchConfig.objects.create(device=device, text=result, created=datetime.now())

    return result
