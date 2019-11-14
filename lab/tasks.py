from celery import shared_task
from netmiko import Netmiko
from datetime import datetime
from hier_config.host import Host
from .models import Device
from .models import DevicePair
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

    if device.environment == "PROD":
        host = {
            "host": device.name,
            "username": username,
            "password": password,
            "device_type": platform_mapper[device.os_type]
        }
        nm = Netmiko(**host)
        nm.send_command("terminal length 0")
        result = nm.send_command(command)
    else:
        device_pair = DevicePair.objects.get(id=device_id)
        other_device = device_pair.prod_device
        interface_maps = InterfaceMapper.objects.filter(
            prod_device=other_device,
            lab_device=device
        )
        interface_replace_map = list()

        for item in interface_maps:
            interface_replace_maps.append(
                {"search": item.prod_device.name, "replace": item.lab_device.name}
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
            "per_line_sub": interface_replace_map,
            "idempotent_commands_blacklist": [],
            "idempotent_commands": [],
            "negation_default_when": [],
            "negation_negate_with": [],
        }
        prod_config = RouteSwitchConfig.objects.get(id=other_device.id)
        host = Host(device.name, os=device.os_type, hconfig_options=options)
        host.load_running_config(name=prod_config.text, config_type="running", load_file=False)
        result = str()

        for line in host.running_config.all_children():
            result += line.cisco_style_text()

    try:
        RouteSwitchConfig.objects.get(device=device)
        RouteSwitchConfig.objects.update(device=device, text=result)
    except RouteSwitchConfig.DoesNotExist:
        RouteSwitchConfig.objects.create(device=device, text=result, created=datetime.now())

    return result
