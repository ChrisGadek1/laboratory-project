from django.shortcuts import render
from .forms import SampleForm, ResearchForm
# Create your views here.


def main_site(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'main_logged.html', {})
    else:
        return render(request, 'main_not_logged.html', {})


def sample_add(request, *args, **kwargs):
    form = SampleForm(request.POST or None)
    if form.is_valid():
        form.save()

    contex = {
        "form1" : SampleForm,
    }

    return render(request, 'sample_add.html', contex)


def research_add(request, *args, **kwargs):
    form = SampleForm(request.POST or None)
    if form.is_valid():
        form.save()

    contex = {
        "form2": ResearchForm,
    }

    return render(request, 'research_add.html', contex)