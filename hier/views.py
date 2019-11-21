from django.shortcuts import render
from django.http import (
    HttpResponseRedirect,
    HttpResponse
)
from hier.models import Lineage


def hier(request):
    return HttpResponseRedirect('/hier/lineages')


def get_lineage(request):
    lineages = Lineage.objects.all()
    context = {
        "lineages": lineages,
    }
    return render(request, 'hier/lineages.html', context)
