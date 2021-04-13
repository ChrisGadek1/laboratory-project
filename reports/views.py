from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from samples.forms import SampleForm, ResearchForm

# Create your views here.


def choose_mode(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'reports/choose_mode.html', {})
    else:
        return render(request, 'main_not_logged.html', {})


def add_template(request, *args, **kwargs):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST" and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
        else:
            samples_labels = {v: k for k, v in SampleForm.Meta.labels.items()}
            research_labels = {v: k for k, v in ResearchForm.Meta.labels.items()}
            context = {
                "samples_fields": samples_labels,
                "research_fields": research_labels
            }
        return render(request, 'reports/add_template.html', context)
    else:
        return render(request, 'main_not_logged.html', {})


def generate_report(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'reports/reports.html', {})
    else:
        return render(request, 'main_not_logged.html', {})