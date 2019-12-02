from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from rest_framework import viewsets
from lab.models import (
    Device,
    DevicePair,
    DeviceInterface,
    InterfaceMapper,
    RouteSwitchConfig,
    OperatingSystem,
)
from lab.tasks import (
    fetch_production_config,
    fetch_lab_config,
    fetch_interfaces,
    fetch_or_update
)
from lab.serializers import (
    DeviceSerializer,
    DevicePairSerializer,
    DeviceInterfaceSerializer,
    InterfaceMapperSerializer,
    RouteSwitchConfigSerializer,
)


def devices(request):
    device_list = Device.objects.all()
    operating_systems = OperatingSystem.objects.all()
    context = {
        'devices': device_list,
        'operating_systems': operating_systems,
    }
    return render(request, 'lab/devices.html', context)


def device(request, device_id=None):
    if request.user.is_authenticated:
        device = Device.objects.get(id=device_id)
        interfaces = DeviceInterface.objects.filter(device=device)

        try:
            config = RouteSwitchConfig.objects.get(device=device)
            config = config.text
        except RouteSwitchConfig.DoesNotExist:
            config = str()

        if device.environment == "PROD":
            device_pair = DevicePair.objects.get(prod_device=device)
            other_device = device_pair.lab_device
            interface_maps = InterfaceMapper.objects.filter(prod_device__device__name=device.name)
        else:
            device_pair = DevicePair.objects.get(lab_device=device)
            other_device = device_pair.prod_device
            interface_maps = InterfaceMapper.objects.filter(lab_device__device__name=device.name)

        eligible_interfaces = DeviceInterface.objects.filter(device=other_device)

        if request.method == 'POST':
            if request.POST['name']:
                messages.success(request, f"{device.name} has been updated to {request.POST['name']}")
                device.name = request.POST['name']
            if request.POST['environment']:
                messages.success(request, f"{request.POST['environment']} has been updated on {device.name}")
                device.environment = request.POST['environment']
            if request.POST['os_type']:
                os = OperatingSystem.objects.filter(name=request.POST['os_type'])
                if os:
                    messages.success(request, f"{request.POST['os_type']} has been updated on {device.name}")
                    device.os_type = os[0]
                else:
                    messages.warning(request, f"invalid operating sytem - {request.POST['os_type']}")
                    messages.info(request, f"valid choices: {[os.name for os in OperatingSystem.objects.all()]}")
            device.save()

        context = {
            'device': device,
            'interfaces': interfaces,
            'interface_maps': interface_maps,
            'eligible_interfaces': eligible_interfaces,
            'device_config': config,
        }

        return render(request, 'lab/device.html', context)
    return HttpResponseRedirect('/user/login/')


def device_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            os = OperatingSystem.objects.get(id=request.POST['os_type'])
            prod_device = Device.objects.create(
                name=request.POST['name'],
                environment="PROD",
                os_type=os
            )
            lab_device = Device.objects.create(
                name=request.POST['name'],
                environment="LAB",
                os_type=os
            )
            DevicePair.objects.create(prod_device=prod_device, lab_device=lab_device)

            messages.success(request, f"{request.POST['name']} has been created")

        return HttpResponseRedirect('/devices/')
    return HttpResponseRedirect('/user/login/')


def device_delete(request, device_id=None):
    if request.user.is_authenticated:
        device = Device.objects.get(id=device_id)

        if device.environment == "PROD":
            device_pair = DevicePair.objects.get(prod_device=device)
            other_device = device_pair.lab_device
        else:
            device_pair = DevicePair.objects.get(lab_device=device)
            other_device = device_pair.prod_device

        device_name = device.name

        device.delete()
        other_device.delete()
        messages.success(request, f"{device_name} has been deleted")
        return HttpResponseRedirect('/devices/')
    return HttpResponseRedirect('/user/login/')


def interface_add(request, device_id=None):
    if request.user.is_authenticated:
        device = Device.objects.get(id=device_id)
        if request.method == 'POST':
            DeviceInterface.objects.create(name=request.POST['name'], device=device)

        messages.success(request, f"interface {request.POST['name']} has been created on {device.name}")

        return HttpResponseRedirect(f"/devices/{device.id}/")
    return HttpResponseRedirect('/user/login/')


def interface_delete(request, device_id=None, interface_id=None):
    if request.user.is_authenticated:
        interface = DeviceInterface.objects.get(id=interface_id)
        interface_name = interface.name
        device = Device.objects.get(id=device_id)

        interface.delete()
        messages.success(request, f"{interface_name} deleted from {device.name}")

        return HttpResponseRedirect(f"/devices/{device.id}")
    return HttpResponseRedirect('/user/login/')


def interface_fetch(request, device_id=None):
    if request.user.is_authenticated:
        result = fetch_interfaces.delay(device_id=device_id)
        print(result)
        return HttpResponseRedirect(f"/devices/{device_id}")
    return HttpResponseRedirect('/user/login/')


def interface_mapper_add(request, device_id=None):
    if request.user.is_authenticated:
        lab_interface = DeviceInterface.objects.get(id=request.POST['lab_device'])
        prod_interface = DeviceInterface.objects.get(id=request.POST['prod_device'])

        InterfaceMapper.objects.create(prod_device=prod_interface, lab_device=lab_interface)
        messages.success(
            request,
            f"mapped {prod_interface.device.name} - {prod_interface.name} to {lab_interface.device.name} - {lab_interface.name}"
        )
        return HttpResponseRedirect(f"/devices/{device_id}")
    return HttpResponseRedirect('/user/login/')


def interface_mapper_delete(request, device_id=None, interface_mapper_id=None):
    if request.user.is_authenticated:
        interface_map = InterfaceMapper.objects.get(id=interface_mapper_id)
        device = Device.objects.get(id=device_id)

        interface_map.delete()
        messages.success(request, f"interface map has been deleted for {device.name}")

        return HttpResponseRedirect(f"/devices/{device_id}")
    return HttpResponseRedirect('/user/login/')


def device_config(request, device_id=None):
    if request.user.is_authenticated:
        device = Device.objects.get(id=device_id)
        if request.method == "POST":
            if device.environment == "PROD":
                fetch_production_config.delay(
                    device_id=device_id,
                    username=request.POST['username'],
                    password=request.POST['password'],
                )
            else:
                fetch_lab_config.delay(device_id=device_id)

            messages.success(request, f"config being fetched for {device.name}")

        return HttpResponseRedirect(f"/devices/{device_id}")
    return HttpResponseRedirect('/user/login/')


def device_config_manually(request, device_id=None):
    if request.user.is_authenticated:
        device = Device.objects.get(id=device_id)
        fetch_or_update(device=device, config=request.POST['text'])

        return HttpResponseRedirect(f"/devices/{device_id}")
    return HttpResponseRedirect('/user/login/')


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceInterfaceViewSet(viewsets.ModelViewSet):
    queryset = DeviceInterface.objects.all()
    serializer_class = DeviceInterfaceSerializer


class DevicePairViewSet(viewsets.ModelViewSet):
    queryset = DevicePair.objects.all()
    serializer_class = DevicePairSerializer


class InterfaceMapperViewSet(viewsets.ModelViewSet):
    queryset = InterfaceMapper.objects.all()
    serializer_class = InterfaceMapperSerializer


class RouteSwitchConfigViewSet(viewsets.ModelViewSet):
    queryset = RouteSwitchConfig.objects.all()
    serializer_class = RouteSwitchConfigSerializer
