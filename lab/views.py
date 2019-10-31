from django.shortcuts import render
from django.http import HttpResponse
from .models import Device


def devices(request, id=None):
    device_list = Device.objects.all()
    context = {'devices': device_list}
    return render(request, 'lab/devices.html', context)

def device(request, id=None):
    device = Device.objects.get(id=id)
    context = {'device': device}
    return render(request, 'lab/device.html', context)

def device_add(request):
    context = {'device': None}
    return render(request, 'lab/device.html', context)

def device_modify(request, id=None):
    device = Device.objects.get(id=id)
    context = {'device': device}
    return render(request, 'lab/device.html', context)

def device_delete(request, id=None):
    return HttpResponse('<html><body>Delete Device</body></html>')

def interface_add(request):
    return HttpResponse('<html><body>Add Interface</body></html>')

def interface_modify(request):
    return HttpResponse('<html><body>Modify Interface</body></html>')

def interface_delete(request):
    return HttpResponse('<html><body>Delete Interface</body></html>')

def interface_mapper_add(request):
    return HttpResponse('<html><body>Interface Mapper Add</body></html>')

def interface_mapper_modify(request):
    return HttpResponse('<html><body>Interface Mapper Modify</body></html>')

def interface_mapper_delete(request):
    return HttpResponse('<html><body>Interface Mapper Delete</body></html>')

def console_servers(request):
    return HttpResponse('<html><body>Console Servers</body></html>')

def console_servers_add(request):
    return HttpResponse('<html><body>Console Servers Add</body></html>')

def console_servers_modify(request):
    return HttpResponse('<html><body>Console Servers Modify</body></html>')

def console_servers_delete(request):
    return HttpResponse('<html><body>Console Servers Delete</body></html>')

def console_port_add(request):
    return HttpResponse('<html><body>Console Port Add</body></html>')

def console_port_modify(request):
    return HttpResponse('<html><body>Console Port Modify</body></html>')

def console_port_delete(request):
    return HttpResponse('<html><body>Console Port Delete</body></html>')