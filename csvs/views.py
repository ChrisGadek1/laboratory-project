import re
import codecs
import zipfile
from io import BytesIO
from django.contrib.messages import get_messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from samples.models import Sampling, Research, Type, ControlType, WIJHARS, ResearchStatus, MetodAndNorm, DeliveryWay
from csvs.forms import CsvOptionsAction
import csv
from django.contrib import messages
from datetime import datetime
from django.forms.models import model_to_dict

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
                request.session['mode'] = None
                return HttpResponseRedirect('read_csv/')

    if request.user.is_authenticated:
        return render(request, 'csvs/choose_mode_csv.html', {"form": form})
    else:
        return render(request, 'main_not_logged.html', {})


def handle_object(mode, obj_name):
    if   mode == 'Control type':
        obj_handle = ControlType.objects.get(name=obj_name)
    elif mode == 'Metod and norm':
        obj_handle = MetodAndNorm.objects.get(name=obj_name)
    elif mode == 'Research status':
        obj_handle = ResearchStatus.objects.get(name=obj_name)
    elif mode == 'Research':
        obj_handle = Research.objects.get(name=obj_name)
    elif mode == "Sampling":
        obj_handle = Sampling.objects.get(code=obj_name)
    elif mode == 'Type':
        obj_handle = Type.objects.get(name=obj_name)
    elif mode == 'Wijhars':
        obj_handle = WIJHARS.objects.get(name=obj_name)
    elif mode == 'Delivery Way':
        obj_handle = DeliveryWay.objects.get(name=obj_name)
    else:
        obj_handle = None

    if mode == 'Research':
        labels = ['sampling',       'name',             'marking',                   'nutritional_value',   'specification',
                  'ordinance',      'samples_number',   'result',                    'start_date',          'research_completion_date',
                  'status',         'uncertainty',      'summary_meet_requirements', 'requirementsType',    'summary_requirements_explains',
                  'requirements',   'unit']
        source = [obj_handle.sampling.code, obj_handle.name,            obj_handle.marking, obj_handle.nutritional_value,   obj_handle.specification,
                  obj_handle.ordinance,     obj_handle.samples_number,  obj_handle.result,  obj_handle.start_date,          obj_handle.research_completion_date,
                  obj_handle.status.name,   obj_handle.uncertainty,     obj_handle.summary_meet_requirements,   obj_handle.requirementsType,
                  obj_handle.summary_requirements_explains,             obj_handle.requirements,                obj_handle.unit]

    elif mode == "Sampling":
        labels = ['number',              'code',                   'WIJHARS',                   'assortment',                'admission_date',
                  'expiration_date',     'completion_date',        'additional_comment',        'customer_name',             'size',
                  'condition',           'appeal_analysis',        'control_type',              'type',                      'sampling_method',
                  'manufacturer_name',   'manufacturer_address',   'sample_getter1_name',       'sample_getter1_surname',    'sample_getter1_position',
                  'sample_getter2_name', 'sample_getter2_surname', 'sample_getter2_position',   'manufacturer',              'final_consumer',
                  'consumer_name',       'consumer_address',       'order_number',              'mechanism_name_and_symbol', 'sample_delivery',
                  'is_OK',               'if_not_why',             'recipient',                 'agreement_number',          'collection_date',
                  'case_number',         'delivery_date',          'type_of_package',           'batch_size',                'batch_number',
                  'batch_production_date']
        source = [obj_handle.number,                    obj_handle.code,                   obj_handle.WIJHARS.name,            obj_handle.assortment,
                  obj_handle.admission_date,            obj_handle.expiration_date,        obj_handle.completion_date,         obj_handle.additional_comment,
                  obj_handle.customer_name,             obj_handle.size,                   obj_handle.condition,               obj_handle.appeal_analysis,
                  obj_handle.control_type.name,         obj_handle.type.name,              obj_handle.sampling_method.name,    obj_handle.manufacturer_name,
                  obj_handle.manufacturer_address,      obj_handle.sample_getter1_name,    obj_handle.sample_getter1_surname,  obj_handle.sample_getter1_position,
                  obj_handle.sample_getter2_name,       obj_handle.sample_getter2_surname, obj_handle.sample_getter2_position, obj_handle.manufacturer,
                  obj_handle.final_consumer,            obj_handle.consumer_name,          obj_handle.consumer_address,        obj_handle.order_number,
                  obj_handle.mechanism_name_and_symbol, obj_handle.sample_delivery.name,   obj_handle.is_OK,                   obj_handle.if_not_why,
                  obj_handle.recipient,                 obj_handle.agreement_number,       obj_handle.collection_date,         obj_handle.case_number,
                  obj_handle.delivery_date,             obj_handle.type_of_package,        obj_handle.batch_size,              obj_handle.batch_number,
                  obj_handle.batch_production_date]

    elif mode == 'Type' or mode == 'Wijhars' or mode == 'Delivery Way' or \
            mode == 'Control type' or mode == 'Metod and norm' or mode == 'Research status':
        labels = ['name']
        source = [obj_handle.name]

    else:
        labels = ['Error']
        source = ['Error']

    return obj_handle, labels, source


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
        elif mode == 'All':
            context = {
                        "Control type": ControlType.objects.all(),       "Metod and norm": MetodAndNorm.objects.all(),
                        "Research status": ResearchStatus.objects.all(), "Type": Type.objects.all(),
                        "Wijhars": WIJHARS.objects.all(),                "Delivery Way": DeliveryWay.objects.all(),
                        "Sampling": Sampling.objects.all(),              "Research":  Research.objects.all()
                        }
        else:
            context = {"Object": None}

        if request.method == "POST":

            if mode == 'All':
                zipped_file = BytesIO()
                with zipfile.ZipFile(zipped_file, 'a', zipfile.ZIP_DEFLATED) as zipped:

                    for object_type in context:
                        file_name = object_type + ".csv"
                        with open(file_name, 'w+', newline='', encoding='utf-8') as csv_data:

                            writer = csv.writer(csv_data, delimiter=';')
                            writer.writerow('')

                            objects = context[object_type]

                            for obj_name in objects.iterator():
                                obj_handle, labels, source = handle_object(object_type, obj_name)

                                for i in range(len(labels)):
                                    writer.writerow([labels[i], source[i]])
                                writer.writerow("")

                            csv_data.seek(0)
                            zipped.writestr("{}.csv".format(object_type), csv_data.read())

                zipped_file.seek(0)
                response = HttpResponse(zipped_file, content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=kopia_calej_bazy.zip'

            else:
                obj_handle, labels, source = handle_object(mode, request.POST.get("obj_position", ""))

                response = HttpResponse(content_type='text/csv')
                response.write(u'\ufeff'.encode('utf8'))
                writer = csv.writer(response, delimiter=';')
                writer.writerow('')

                if mode == 'Sampling':
                    file_name = mode + "_" + obj_handle.code + ".csv"
                elif mode == 'Error':
                    file_name = "Error.csv"
                else:
                    file_name = mode+".csv"

                response['Content-Disposition'] = 'attachment; filename=' + file_name

                for i in range(len(labels)):
                    writer.writerow([labels[i], source[i]])
                writer.writerow(['', ''])

            return response

        return render(request, 'csvs/to_csvs.html', context)
    else:
        return render(request, 'main_not_logged.html', {})


def find_data_format(data_string):
    if '.' in data_string:
        if len(data_string) > 8:
            data_format = '%d.%m.%Y'
        else:
            data_format = '%d.%m.%y'
    elif '-' in data_string:
        if len(data_string) > 8:
            data_format = '%Y-%m-%d'
        else:
            data_format = '%y-%m-%d'
    else:
        data_format = 'error'
    return data_format


def take_data_into_object(mode, dict, request):
    if mode == 'Control type':
        try:
            ControlType.objects.get(name=dict['name'])
        except ControlType.DoesNotExist as error:
            obj = ControlType()
            obj.name = dict['name']
            obj.save()
    elif mode == 'Delivery Way':
        try:
            DeliveryWay.objects.get(name=dict['name'])
        except DeliveryWay.DoesNotExist as error:
            obj = DeliveryWay()
            obj.name = dict['name']
            obj.save()
    elif mode == 'Metod and norm':
        try:
            MetodAndNorm.objects.get(name=dict['name'])
        except MetodAndNorm.DoesNotExist as error:
            obj = MetodAndNorm()
            obj.name = dict['name']
            obj.save()
    elif mode == 'Research status':
        try:
            ResearchStatus.objects.get(name=dict['name'])
        except ResearchStatus.DoesNotExist as error:
            obj = ResearchStatus()
            obj.name = dict['name']
            obj.save()
    elif mode == 'Research':
        try:
            Research.objects.get(name=dict['name'])
        except Research.DoesNotExist as error:
            obj = Research()
            for key_obj in model_to_dict(Research):

                if key_obj == "id":
                    continue

                if key_obj == "sampling":
                    obj.sampling = Sampling.objects.get(code=dict['sampling'])
                elif key_obj == "status":
                    obj.status = ResearchStatus.objects.get(name=dict['status'])
                elif key_obj == "start_date" or key_obj == "research_completion_date":
                    try:
                        obj.start_date = datetime.strptime(dict['start_date'], find_data_format(dict['start_date']))
                        obj.research_completion_date = datetime.strptime(dict['research_completion_date'],
                                                                         find_data_format(dict['research_completion_date']))
                    except ValueError as error:
                        contents = "Podane daty dla badania " + dict['name'] + \
                                   " są w nieprawidłowym formacie. \r\n Prawidłowe formaty dla daty to: \r\n YYYY-MM-DD, YY-MM-DD, DD-MM-YY, DD-MM-YYYY"
                        messages.add_message(request, messages.ERROR, contents)
                        return
                else:
                    obj.__setattr__(key_obj, dict[key_obj])
            obj.save()
    elif mode == "Sampling":
        try:
            Sampling.objects.get(number=dict['number'])
        except Sampling.DoesNotExist as error:
            obj = Sampling()
            for key_obj in model_to_dict(Sampling):
                if key_obj == "id":
                    continue

                if key_obj == "WIJHARS":
                    obj.WIJHARS = WIJHARS.objects.get(name=dict['WIJHARS'])
                elif key_obj == "control_type":
                    obj.control_type = ControlType.objects.get(name=dict['control_type'])
                elif key_obj == "type":
                    obj.type = Type.objects.get(name=dict['type'])
                elif key_obj == "sampling_method":
                    obj.sampling_method = MetodAndNorm.objects.get(name=dict['sampling_method'])
                elif key_obj == "sample_delivery":
                    obj.sample_delivery = DeliveryWay.objects.get(name=dict['sample_delivery'])
                elif key_obj == "admission_date" or key_obj == "expiration_date" or key_obj == "completion_date"\
                        or key_obj == "collection_date" or key_obj == "delivery_date" or key_obj == "batch_production_date":
                    try:
                        obj.start_date = datetime.strptime(dict['admission_date'],
                                                           find_data_format(dict['admission_date']))
                        obj.expiration_date = datetime.strptime(dict['expiration_date'],
                                                                find_data_format(dict['expiration_date']))
                        obj.completion_date = datetime.strptime(dict['completion_date'],
                                                                find_data_format(dict['completion_date']))
                        obj.collection_date = datetime.strptime(dict['collection_date'],
                                                                find_data_format(dict['collection_date']))
                        obj.delivery_date = datetime.strptime(dict['delivery_date'],
                                                                find_data_format(dict['delivery_date']))
                        obj.batch_production_date = datetime.strptime(dict['batch_production_date'],
                                                                find_data_format(dict['batch_production_date']))
                    except ValueError as error:
                        contents = "Podane daty dla próbki " + dict['number'] + \
                                   " są w nieprawidłowym formacie. \r\n Prawidłowe formaty dla daty to: \r\n YYYY-MM-DD, YY-MM-DD, DD-MM-YY, DD-MM-YYYY"
                        messages.add_message(request, messages.ERROR, contents)
                        return
                else:
                    obj.__setattr__(key_obj, dict[key_obj])
            obj.save()
    elif mode == 'Type':
        try:
            Type.objects.get(name=dict['name'])
        except Type.DoesNotExist as error:
            obj = Type()
            obj.name = dict['name']
            obj.save()
    elif mode == 'Wijhars':
        try:
            WIJHARS.objects.get(name=dict['name'])
        except WIJHARS.DoesNotExist as error:
            obj = WIJHARS()
            obj.name = dict['name']
            obj.save()


def read_csv(request, *args, **kwargs):

    write_messages = 0

    if request.session.get('mode'):
        mode = request.session.get('mode')
    else:
        mode = ''
        storage = get_messages(request)
        for message in storage:
            mode = str(message)
        request.session['mode'] = mode

    print("mode:", mode)

    if request.method == "POST":
        if request.FILES:
            file_reader = csv.reader(codecs.iterdecode(request.FILES['file_input'], 'utf-8', errors='replace'), delimiter=';')
            to_first_data = 0
            dict = {}
            for row in file_reader:
                if row and re.search("[a-zA-Z]+", row[0]):
                    dict[row[0]] = row[1]
                    to_first_data = 1
                elif to_first_data:
                    take_data_into_object(mode, dict, request)
                    dict = {}
                    to_first_data = 0
        write_messages = 1

    if request.user.is_authenticated:
        return render(request, 'csvs/from_csv.html', context={"contains_errors": write_messages})
    else:
        return render(request, 'main_not_logged.html', context={})