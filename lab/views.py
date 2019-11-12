from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import DEVICE_ENVIRONMENT
from .models import Device
from .models import DeviceInterface


def devices(request):
    device_list = Device.objects.all()
    context = {
        'devices': device_list,
    }
    return render(request, 'lab/devices.html', context)

def device(request, device_id=None):
    device = Device.objects.get(id=device_id)
    interfaces = DeviceInterface.objects.filter(device=device)

    if request.method == 'POST':
        if request.POST['name']:
            messages.success(request, f"{device.name} has been updated to {request.POST['name']}")
            device.name = request.POST['name']
        if request.POST['environment']:
            messages.success(request, f"{request.POST['environment']} has been updated on {device.name}")
            device.environment = request.POST['environment']
        if request.POST['os_type']:
            messages.success(request, f"{request.POST['os_type']} has been updated on {device.name}")
            device.os_type = request.POST['os_type']
        device.save()

    context = {
        'device': device,
        'interfaces': interfaces,
        'environments': DEVICE_ENVIRONMENT,
        }

    return render(request, 'lab/device.html', context)

def device_add(request):
    if request.method == 'POST':
        print(request.POST)
        Device.objects.create(
            name=request.POST['name'],
            environment=request.POST['environment'],
            os_type=request.POST['os_type']
        )
    messages.success(request, f"{request.POST['name']} has been created")
    return HttpResponseRedirect('/devices/')

def device_delete(request, device_id=None):
    device = Device.objects.get(id=device_id)
    device_name = device.name
    device.delete()
    messages.success(request, f"{device_name} has been deleted")
    return HttpResponseRedirect('/devices/')

def interface_add(request, device_id=None):
    device = Device.objects.get(id=device_id)
    if request.method == 'POST':
        DeviceInterface.objects.create(name=request.POST['name'], device=device)

    messages.success(request, f"interface {request.POST['name']} has been created on {device.name}")
    return HttpResponseRedirect(f"/devices/{device.id}/")

def interface_delete(request, device_id=None, interface_id=None):
    interface = DeviceInterface.objects.get(id=interface_id)
    interface_name = interface.name
    device = Device.objects.get(id=device_id)
    interface.delete()
    messages.success(request, f"{interface_name} deleted from {device.name}")
    return HttpResponseRedirect(f"/devices/{device.id}")