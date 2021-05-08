from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from docx.oxml.ns import qn

from samples.forms import SampleForm, ResearchForm
import os
from samples.models import Sampling, WIJHARS, MetodAndNorm, ControlType, DeliveryWay, Type, Research, ResearchStatus
from docx import Document, table
from docx.oxml import OxmlElement
import copy
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

        def remove_row(table, row):
            tbl = table._tbl
            tr = row._tr
            tbl.remove(tr)

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
            document = Document("media/"+request.POST.get("template", ""))


            #inserting data about samples:
            for paragraph in document.paragraphs:
                for prop in sample_values.keys():
                    if "{{"+prop+"}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{"+prop+"}}", sample_values[prop])
            for table_v in document.tables:
                for column in table_v.columns:
                    for cell in column.cells:
                        for prop in sample_values.keys():
                            if "{{" + prop + "}}" in cell.text:
                                cell.text = cell.text.replace("{{" + prop + "}}", sample_values[prop])

            #inserting data about researches:

            researches = list(Research.objects.filter(sampling=sample).all())
            props = []
            if len(researches) > 0:
                props = researches[0].__dict__.keys()
            insert_flag = False
            columns = []
            cells = []
            rows_to_delete = []
            merge_flag = True
            for table_v in document.tables:
                for row in table_v.rows:
                    if not insert_flag:
                        for cell in row.cells:
                            if "{{init_researches}}" in cell.text:
                                insert_flag = True
                                rows_to_delete.append((table_v, row))
                    else:
                        cell_index = 0
                        for cell in row.cells:
                            cells.append(cell)
                            columns.append([])
                            has_prop_flag = False
                            for prop in props:
                                if "{{" + prop + "}}" in cell.text:
                                    columns[cell_index].append(prop)
                                    has_prop_flag = True
                            if not has_prop_flag:
                                if "{{incr}}" in cell.text:
                                    columns[cell_index].append("incr")
                                else:
                                    columns[cell_index].append(cell.text)
                            cell_index += 1
                        rows_to_delete.append((table_v, row))
                        #print(table_v._element.xml)
                        for it, research in enumerate(researches, start=1):
                            row_tmp = table_v.add_row()
                            new_row = row_tmp.cells
                            cells_copy = copy.deepcopy(cells)
                            #word manipulation:
                            print(columns)
                            for i in range(len(columns)):
                                print(i)
                                tc = new_row[i]._tc
                                tcPr = tc.tcPr
                                borders = OxmlElement('w:tcBorders')
                                border_list = ['w:left', 'w:right', 'w:top', 'w:bottom']
                                for border_element in border_list:
                                    element = OxmlElement(border_element)
                                    element.set(qn('w:val'), 'single')
                                    element.set(qn('w:sz'), '4')
                                    element.set(qn('w:space'), '0')
                                    element.set(qn('w:color'), '000000')
                                    borders.append(element)
                                tcPr.append(borders)
                                for replaceable in columns[i]:
                                    if replaceable in props:
                                        print("{{"+replaceable+"}}", research.__dict__.get(replaceable))
                                        text = cells_copy[i].text
                                        print("poprzedni tekst:",text)
                                        new_row[i].text = text.replace("{{"+replaceable+"}}", str(research.__dict__.get(replaceable)))
                                        cells_copy[i].text = new_row[i].text
                                        print("po zmianie",new_row[i].text)
                                    elif replaceable == "incr":
                                        new_row[i].text = str(it)
                                    else:
                                        new_row[i].text = replaceable

                            for i in range(len(new_row) - 1, 0, -1):
                                if i > 0 and new_row[i].text == new_row[i-1].text:
                                    text = new_row[i].text
                                    new_row[i].text = ""
                                    new_row[i].merge(new_row[i-1])
                                    new_row[i-1].text = text

                        insert_flag = False
                        columns = []
                        cells = []
                        break
            for data in rows_to_delete:
                if data[1]._element.getparent() is not None:
                    data[1]._element.getparent().remove(data[1]._element)
            document.save("generated_reports/report.docx")
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=report.docx'
            document.save(response)
            return response

        return render(request, 'reports/reports.html', context)
    else:
        return render(request, 'main_not_logged.html', {})