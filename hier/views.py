from django.shortcuts import render
from django.contrib import messages
from django.views.generic import (
    CreateView
)
from django.http import (
    HttpResponseRedirect,
)
from hier.models import (
    Lineage,
    LINEAGE_CHOICES
)


def hier(request):
    return HttpResponseRedirect('/hier/lineages/')


def get_lineage(request):
    if request.method == "GET":
        print(request.GET)
        kwargs = {
            # 'parent': request.GET.get('parent', None),
            'key': request.GET.get('key', None),
            'value': request.GET.get('value', None),
            'os': request.GET.get('os', None),
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        kwargs = {k: v for k, v in kwargs.items() if v is not ''}
        lineages = Lineage.objects.filter(**kwargs)

    context = {
        "lineages": lineages,
        "lineage_choices": LINEAGE_CHOICES,
    }

    return render(request, 'hier/lineages.html', context)


def add_lineage(request):
    if request.method == "POST":
        data = {
            'parent': request.POST['parent'],
            'key': request.POST['key'],
            'value': request.POST['value'],
            'os': request.POST['os'],
        }
        print(data)
        if data['parent'] == "":
            data['parent'] = None
        Lineage.objects.create(
            parent=data['parent'],
            key=data['key'],
            value=data['value'],
            os=data['os']
        )
    messages.success(request, f"lineage rule created: {data['key']}:{data['value']}")

    return HttpResponseRedirect('/hier/lineages/')


def delete_lineage(request, lineage_id=None):
    lineage = Lineage.objects.get(id=lineage_id)
    lineage.delete()

    messages.success(request, f"lineage rule deleted")

    return HttpResponseRedirect('/hier/lineages/')
