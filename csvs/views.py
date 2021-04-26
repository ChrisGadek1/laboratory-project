import codecs

from django.contrib.messages import get_messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from samples.models import Sampling, Research, Type, ControlType, WIJHARS, ResearchStatus, MetodAndNorm, DeliveryWay
from csvs.forms import CsvOptionsAction
import csv
from django.contrib import messages
from datetime import datetime

# Create your views here.


def choose_mode_csv(request, *args, **kwargs):
    form = CsvOptionsAction(data=request.POST)

    if request.method == 'POST':
        if form.is_valid():
            if form['mode'].value() == "Write":
                messages.add_message(request, messages.INFO, form['option'].value())
                return HttpResponseRedirect('csv/')
            elif form['mode'].value() == "Read":
                messages.add_message(request, messages.INFO, form['option'].value())
                return HttpResponseRedirect('read_csv/')

    if request.user.is_authenticated:
        return render(request, 'csvs/choose_mode_csv.html', {"form": form})
    else:
        return render(request, 'main_not_logged.html', {})


def generate_csv(request, *args, **kwargs):
    mode = ''
    storage = get_messages(request)
    for message in storage:
        mode = str(message)
    messages.add_message(request, messages.INFO, mode)

    if request.user.is_authenticated:
        if mode == 'Control type':
            context = {"Object": ControlType.objects.all()}
        elif mode == 'Metod and norm':
            context = {"Object": MetodAndNorm.objects.all()}
        elif mode == 'Research status':
            context = {"Object": ResearchStatus.objects.all()}
        elif mode == 'Research':
            context = {"Object": Research.objects.all()}
        elif mode == "Sampling":
            context = {"Object": Sampling.objects.all()}
        elif mode == 'Type':
            context = {"Object": Type.objects.all()}
        elif mode == 'Wijhars':
            context = {"Object": WIJHARS.objects.all()}
        elif mode == 'Delivery Way':
            context = {"Object": DeliveryWay.objects.all()}
        else:
            context = {"Object": None}

        if request.method == "POST":
            if mode == 'Control type':
                obj_handle = ControlType.objects.get(name=request.POST.get("obj_position", ""))
                labels = ['name']
                source = [obj_handle.name]
                file_name = mode + "_" + obj_handle.name + ".csv"
            elif mode == 'Metod and norm':
                obj_handle = MetodAndNorm.objects.get(name=request.POST.get("obj_position", ""))
                labels = ['name']
                source = [obj_handle.name]
                file_name = mode + "_" + obj_handle.name + ".csv"
            elif mode == 'Research status':
                obj_handle = ResearchStatus.objects.get(name=request.POST.get("obj_position", ""))
                labels = ['name']
                source = [obj_handle.name]
                file_name = mode + "_" + obj_handle.name + ".csv"
            elif mode == 'Research':
                obj_handle = Research.objects.get(name=request.POST.get("obj_position", ""))
                labels = ['sampling', 'name', 'marking', 'nutritional_value', 'specification',
                          'ordinance', 'samples_number', 'result', 'start_date', 'completion_date',
                          'status', 'uncertainty', 'summary_meet_requirements', 'summary_requirements_explains']
                source = [obj_handle.sampling.code, obj_handle.name, obj_handle.marking, obj_handle.nutritional_value, obj_handle.specification,
                          obj_handle.ordinance, obj_handle.samples_number, obj_handle.result, obj_handle.start_date, obj_handle.completion_date,
                          obj_handle.status.name, obj_handle.uncertainty, obj_handle.summary_meet_requirements, obj_handle.summary_requirements_explains]
                file_name = mode + "_" + obj_handle.name + ".csv"
            elif mode == "Sampling":
                obj_handle = Sampling.objects.get(code=request.POST.get("obj_position", ""))
                labels = ['number', 'code', 'WIJHARS', 'assortment', 'admission_date', 'expiration_date',
                          'completion_date',
                          'additional_comment', 'customer_name', 'size', 'condition', 'appeal_analysis', 'control_type',
                          'type', 'sampling_method', 'manufacturer_name', 'manufacturer_address', 'sample_getter1_name',
                          'sample_getter1_surname', 'sample_getter1_position', 'sample_getter2_name',
                          'sample_getter2_surname',
                          'sample_getter2_position', 'manufacturer', 'final_consumer', 'consumer_name',
                          'consumer_address',
                          'order_number', 'mechanism_name_and_symbol', 'sample_delivery', 'is_OK', 'if_not_why']
                source = [obj_handle.number, obj_handle.code, obj_handle.WIJHARS.name, obj_handle.assortment,
                          obj_handle.admission_date, obj_handle.expiration_date, obj_handle.completion_date,
                          obj_handle.additional_comment, obj_handle.customer_name, obj_handle.size,
                          obj_handle.condition,
                          obj_handle.appeal_analysis, obj_handle.control_type.name,
                          obj_handle.type.name, obj_handle.sampling_method.name, obj_handle.manufacturer_name,
                          obj_handle.manufacturer_address, obj_handle.sample_getter1_name,
                          obj_handle.sample_getter1_surname, obj_handle.sample_getter1_position,
                          obj_handle.sample_getter2_name, obj_handle.sample_getter2_surname,
                          obj_handle.sample_getter2_position, obj_handle.manufacturer, obj_handle.final_consumer,
                          obj_handle.consumer_name, obj_handle.consumer_address,
                          obj_handle.order_number, obj_handle.mechanism_name_and_symbol, obj_handle.sample_delivery.name,
                          obj_handle.is_OK, obj_handle.if_not_why]
                file_name = mode + "_" + obj_handle.code + ".csv"
            elif mode == 'Type':
                obj_handle = Type.objects.get(name=request.POST.get("obj_position", ""))
                labels = ['name']
                source = [obj_handle.name]
                file_name = mode + "_" + obj_handle.name + ".csv"
            elif mode == 'Wijhars':
                obj_handle = WIJHARS.objects.get(name=request.POST.get("obj_position", ""))
                labels = ['name']
                source = [obj_handle.name]
                file_name = mode + "_" + obj_handle.name + ".csv"
            elif mode == 'Delivery Way':
                obj_handle = DeliveryWay.objects.get(name=request.POST.get("obj_position", ""))
                labels = ['name']
                source = [obj_handle.name]
                file_name = mode + "_" + obj_handle.name + ".csv"
            else:
                obj_handle = None
                file_name = "Error.csv"
                labels = ['Error']
                source = ['Error']

            """""""""""""""""""""""""""" Generate .csv file """""""""""""""""""""""""""

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            writer = csv.writer(response, delimiter=';')
            #################writer.writerow(['field', 'value'])#######################
            for i in range(len(labels)):
                writer.writerow([labels[i], source[i]])
            return response

        return render(request, 'csvs/csvs.html', context)
    else:
        return render(request, 'main_not_logged.html', {})


def read_csv(request, *args, **kwargs):

    mode = ''
    storage = get_messages(request)
    for message in storage:
        mode = str(message)
    messages.add_message(request, messages.INFO, mode)

    if request.method == "POST":
        if request.FILES:
            file_reader = csv.reader(codecs.iterdecode(request.FILES['file_input'],'utf-8'), delimiter=';')
            dict = {}
            for row in file_reader:
                dict[row[0]] = row[1]

            obj = None
            if mode == 'Control type':
                obj = ControlType()
                obj.name = dict['name']
                obj.save()
            elif mode == 'Metod and norm':
                obj = MetodAndNorm()
                obj.name = dict['name']
                obj.save()
            elif mode == 'Research status':
                obj = ResearchStatus()
                obj.name = dict['name']
                obj.save()
            elif mode == 'Research':
                obj = Research()

                obj.sampling = Sampling.objects.get(code=dict['sampling'])
                obj.name = dict['name']
                obj.marking = dict['marking']
                obj.nutritional_value = dict['nutritional_value']
                obj.specification = dict['specification']
                obj.ordinance = dict['ordinance']
                obj.samples_number = dict['samples_number']
                obj.result = dict['result']
                obj.start_date = datetime.strptime(dict['start_date'], '%Y-%m-%d')
                obj.completion_date = datetime.strptime(dict['completion_date'], '%Y-%m-%d')
                obj.status = ResearchStatus.objects.get(name=dict['status'])
                obj.uncertainty = dict['uncertainty']
                obj.summary_meet_requirements = dict['summary_meet_requirements']
                obj.summary_requirements_explains = dict['summary_requirements_explains']
                obj.save()
            elif mode == "Sampling":
                obj = Sampling()
                print(dict)
                obj.number = dict['number']
                obj.code = dict['code']
                obj.WIJHARS = WIJHARS.objects.get(name=dict['WIJHARS'])
                obj.assortment = dict['assortment']
                obj.admission_date = datetime.strptime(dict['admission_date'], '%Y-%m-%d')
                obj.expiration_date = datetime.strptime(dict['expiration_date'], '%Y-%m-%d')
                obj.completion_date = datetime.strptime(dict['completion_date'], '%Y-%m-%d')
                obj.additional_comment = dict['additional_comment']
                obj.customer_name = dict['customer_name']
                obj.size = dict['size']
                obj.condition = dict['condition']
                obj.appeal_analysis = dict['appeal_analysis']
                obj.control_type = ControlType.objects.get(name=dict['control_type'])
                obj.type = Type.objects.get(name=dict['type'])
                obj.sampling_method = MetodAndNorm.objects.get(name=dict['sampling_method'])
                obj.manufacturer_name = dict['manufacturer_name']
                obj.manufacturer_address = dict['manufacturer_address']
                obj.sample_getter1_name = dict['sample_getter1_name']
                obj.sample_getter1_surname = dict['sample_getter1_surname']
                obj.sample_getter1_position = dict['sample_getter1_position']
                obj.sample_getter2_name = dict['sample_getter2_name']
                obj.sample_getter2_surname = dict['sample_getter2_surname']
                obj.sample_getter2_position = dict['sample_getter2_position']
                obj.manufacturer = dict['manufacturer']
                obj.final_consumer = dict['final_consumer']
                obj.consumer_name = dict['consumer_name']
                obj.consumer_address = dict['consumer_address']
                obj.order_number = dict['order_number']
                obj.mechanism_name_and_symbol = dict['mechanism_name_and_symbol']
                obj.sample_delivery = DeliveryWay.objects.get(name=dict['sample_delivery'])
                obj.is_OK = dict['is_OK']
                obj.if_not_why = dict['if_not_why']
                obj.save()
            elif mode == 'Type':
                obj = Type()
                obj.name = dict['name']
                obj.save()
            elif mode == 'Wijhars':
                obj = WIJHARS()
                obj.name = dict['name']
                obj.save()
            else:
                pass

    context = {}
    if request.user.is_authenticated:
        return render(request, 'csvs/from_csv.html', context)
    else:
        return render(request, 'main_not_logged.html', {})