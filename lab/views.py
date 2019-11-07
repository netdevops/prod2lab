from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Device


def devices(request, id=None):
    device_list = Device.objects.all()
    context = {'devices': device_list}
    return render(request, 'lab/devices.html', context)

def device(request, id=None):
    device = Device.objects.get(id=id)
    if request.method == 'POST':
        if request.POST['device']:
            device.device = request.POST['device']
        if request.POST['environment']:
            device.environment = request.POST['environment']
        if request.POST['os_type']:
            device.os_type = request.POST['os_type']
        device.save()
    context = {'device': device}
    return render(request, 'lab/device.html', context)

def device_add(request, device=None):
    if request.method == 'POST':
        device = Device.objects.create(device=request.POST['device'],
                                       environment=request.POST['environment'],
                                       os_type=request.POST['os_type'])

    context = {'device': device}
    return render(request, 'lab/device.html', context)

def device_delete(request, id=None):
    device = Device.objects.get(id=id)
    device_name = device.device
    device.delete()
    messages.success(request, f"{device_name} has been deleted!")
    return HttpResponseRedirect('/devices/')

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