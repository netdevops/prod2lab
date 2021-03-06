from celery import shared_task
from netmiko import Netmiko
from datetime import datetime
from hier_config import Host
from lab.models import Device
from lab.models import DevicePair
from lab.models import DeviceInterface
from lab.models import RouteSwitchConfig
from lab.models import InterfaceMapper
from hier.serializers import HierSerializer


@shared_task
def fetch_or_update(device, config):
    try:
        device_config = RouteSwitchConfig.objects.get(device=device)
        device_config.text = config
        device_config.save()
    except RouteSwitchConfig.DoesNotExist:
        device_config = RouteSwitchConfig.objects.create(device=device, text=config)

    return device_config


@shared_task
def fetch_production_config(device_id, username, password):
    device = Device.objects.get(id=device_id)

    host = {
        "host": device.name,
        "username": username,
        "password": password,
        "device_type": device.os_type.netmiko_type
    }
    nm = Netmiko(**host)
    nm.disable_paging(device.os_type.terminal_length_cmd)
    result = nm.send_command(device.os_type.fetch_config_cmd)

    fetch_or_update(device, result)

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
    lab_interface_names = list()

    for item in interface_maps:
        interface_replace_maps.append(
            {"search": f"{item.prod_device.name}$", "replace": item.lab_device.name}
        )
        lab_interface_names.append(item.lab_device.name)

    replace_maps = interface_replace_maps

    options = {
        "style": device.os_type,
        "sectional_overwrite": [],
        "sectional_overwrite_no_negate": [],
        "indent_adjust": [],
        "parent_allows_duplicate_child": [],
        "sectional_exiting": [],
        "full_text_sub": [],
        "per_line_sub": replace_maps,
        "idempotent_commands_blacklist": [],
        "idempotent_commands": [],
        "negation_default_when": [],
        "negation_negate_with": [],
        "ordering": []
    }
    prod_config = RouteSwitchConfig.objects.get(device=other_device)
    host = Host(device.name, os=device.os_type, hconfig_options=options)
    host.load_config_from(name="", config_type="running", load_file=False)
    host.load_config_from(name=prod_config.text, config_type="compiled", load_file=False)
    tags = HierSerializer(os=device.os_type)

    for item in host.compiled_config.get_children("startswith", "interface"):
        if item.text.startswith("interface Loopback"):
            pass
        elif item.text.strip("interface ") in lab_interface_names:
            pass
        else:
            tags.add_lineage({"lineage": [{"startswith": [item.text]}], "add_tags": "ignore"})

    host.load_tags(tags.fetch_lineage(), load_file=False)
    host.load_remediation()

    result = host.filter_remediation(exclude_tags="ignore")

    fetch_or_update(device, result)

    return tags


@shared_task
def fetch_interfaces(device_id=None):
    device = Device.objects.get(id=device_id)

    if device.environment == "LAB":
        return {"interfaces_fetched": False, "reason": "can only fetch production interfaces"}

    try:
        options = {
            "style": device.os_type,
            "sectional_overwrite": [],
            "sectional_overwrite_no_negate": [],
            "indent_adjust": [],
            "parent_allows_duplicate_child": [],
            "sectional_exiting": [],
            "full_text_sub": [],
            "per_line_sub": [],
            "idempotent_commands_blacklist": [],
            "idempotent_commands": [],
            "negation_default_when": [],
            "negation_negate_with": [],
            "ordering": []
        }
        device_config = RouteSwitchConfig.objects.get(device=device)
        host = Host(hostname=device.name, os=device.os_type, hconfig_options=options)
        host.load_config_from(name=device_config.text, config_type="running", load_file=False)
        interfaces = host.running_config.get_children('startswith', 'interface')
        for item in interfaces:
            try:
                DeviceInterface.objects.get(device=device, name=f"{item.text.strip('interface ')}")
            except DeviceInterface.DoesNotExist:
                DeviceInterface.objects.create(device=device, name=f"{item.text.strip('interface ')}")

        return {"interfaces_fetched": True, "reason": "interfaces fetched"}
    except RouteSwitchConfig.DoesNotExist:
        return {"interfaces_fetched": False, "reason": "must fetch production config first"}
