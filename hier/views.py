from django.shortcuts import render
from django.http import (
    HttpResponseRedirect,
)
from hier.models import (
    Lineage,
    LINEAGE_CHOICES
)
from hier.forms import AddLineageForm


def hier(request):
    return HttpResponseRedirect('/hier/lineages/')


def get_lineage(request):
    if request.GET:
        lineages = Lineage.objects.filter()
    else:
        lineages = Lineage.objects.all()
    context = {
        "lineages": lineages,
    }
    return render(request, 'hier/lineages.html', context)


def add_lineage(request):
    if request.method == "POST":
        if form.is_valid():
            form = AddLineageForm(request.POST)

            return HttpResponseRedirect('/hier/lineages/')
    else:
        form = AddLineageForm()

    return render(request, 'hier/modals/add-lineage.html', {"form": form})
