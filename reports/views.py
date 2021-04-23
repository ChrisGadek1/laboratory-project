from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from samples.forms import SampleForm, ResearchForm
import os
from samples.models import Sampling, WIJHARS, MetodAndNorm, ControlType, DeliveryWay, Type
from docx import Document
# Create your views here.


def choose_mode(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'reports/choose_mode.html', {})
    else:
        return render(request, 'main_not_logged.html', {})


def add_template(request, *args, **kwargs):
    context = {}
    if request.user.is_authenticated:
        fs = FileSystemStorage()
        if request.method == "POST" and request.POST.get("mode", "") == "add" and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
        elif request.method == "POST"and request.POST.get("mode", "") == "delete":
            name = request.POST.get("choose-to-delete", "")
            fs.delete(name)

        samples_labels = {v: k for k, v in SampleForm.Meta.labels.items()}
        research_labels = {v: k for k, v in ResearchForm.Meta.labels.items()}
        context = {
            "samples_fields": samples_labels,
            "research_fields": research_labels,
            "reports": os.listdir("media/")
        }
        return render(request, 'reports/add_template.html', context)
    else:
        return render(request, 'main_not_logged.html', {})


def generate_report(request, *args, **kwargs):
    if request.user.is_authenticated:
        context = {}
        context["samples"] = Sampling.objects.all()
        context["reports"] = os.listdir("media/")
        if request.method == "POST":
            sample = Sampling.objects.get(code=request.POST.get("sample", ""))
            sample_values = {}
            for prop in SampleForm.Meta.labels.keys():
                value = ""
                if Sampling.objects.get(code=request.POST.get("sample", "")).__dict__.get(prop) is not None:
                    value = sample.__dict__.get(prop)
                else:
                    if prop == "WIJHARS":
                        value = WIJHARS.objects.get(id=sample.WIJHARS_id).name
                    elif prop == "control_type":
                        value = ControlType.objects.get(id=sample.control_type_id).name
                    elif prop == "sampling_method":
                        value = MetodAndNorm.objects.get(id=sample.sampling_method_id).name
                    elif prop == "sample_delivery":
                        value = DeliveryWay.objects.get(id=sample.sample_delivery_id).name
                    elif prop == "type":
                        value = Type.objects.get(id=sample.type_id).name
                if prop == "is_OK":
                    if value == "YES": value = "Tak"
                    else: value = "Nie"
                sample_values[prop] = str(value)
            #print(sample_values)
            document = Document("media/"+request.POST.get("template", ""))
            for paragraph in document.paragraphs:
                for prop in sample_values.keys():
                    if "{{"+prop+"}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{"+prop+"}}", sample_values[prop])
            for table in  document.tables:
                for column in table.columns:
                    for cell in column.cells:
                        for prop in sample_values.keys():
                            if "{{" + prop + "}}" in cell.text:
                                cell.text = cell.text.replace("{{" + prop + "}}", sample_values[prop])
            document.save("generated_reports/report.docx")
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=report.docx'
            document.save(response)
            return response

        return render(request, 'reports/reports.html', context)
    else:
        return render(request, 'main_not_logged.html', {})