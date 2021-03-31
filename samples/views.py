from django.shortcuts import render
from django.shortcuts import redirect
from .forms import SampleForm, ResearchForm
# Create your views here.


def main_site(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'main_logged.html', {})
    else:
        return render(request, 'main_not_logged.html', {})


def sample_add(request, *args, **kwargs):
    form = SampleForm(request.POST)
    if form.is_valid():
        form.save()

    contex = {
        "form1" : SampleForm,
    }
    if request.user.is_authenticated:
        return render(request, 'sample_add.html', contex)
    else:
        return redirect('/')


def research_add(request, *args, **kwargs):
    form = ResearchForm(request.POST or None)
    print(form.errors)
    if form.is_valid():
        form.save()

    contex = {
        "form2": ResearchForm,
    }
    if request.user.is_authenticated:
        return render(request, 'research_add.html', contex)
    else:
        return redirect('/')