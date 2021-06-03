from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import SampleForm, ResearchForm, ChoiceAction, FindResearch, ControlTypeForm, FindControlType,\
    DeliveryWayForm, FindDeliveryWays, WIJHARSForm, FindWIJHARSs, TypeForm, FindTypes, ResearchStatusForm, FindResearchStatuses, \
    MetodAndNormForm, FindMetodAndNorms
from .models import Sampling, Research, ControlType, DeliveryWay, WIJHARS, Type, ResearchStatus, MetodAndNorm
from django.contrib import messages
from .utils import add_to_database, add_others_to_database

# Create your views here.


def main_site(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'main_logged.html', {})
    else:
        return render(request, 'main_not_logged.html', {})


def sample_add(request, *args, **kwargs):
    contains_error, action, form2, form3, form = add_to_database(request, SampleForm, ResearchForm, Sampling, 'number')

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action,
        "contains_error": contains_error
    }

    if request.is_ajax():
        idx = request.body.decode()
        obj = Sampling.objects.get(id=idx)
        return JsonResponse({
            'number': obj.number,
            'code': obj.code,
            'WIJHARS': obj.WIJHARS_id,
            'assortment': obj.assortment,
            'admission_date': obj.admission_date,
            'completion_date': obj.completion_date,
            'expiration_date': obj.expiration_date,
            'additional_comment': obj.additional_comment,
            'customer_name': obj.customer_name,
            'size': obj.size,
            'condition': obj.condition,
            'appeal_analysis': obj.appeal_analysis,
            'control_type': obj.control_type_id,
            'type': obj.type_id,
            'sampling_method': obj.sampling_method_id,
            'manufacturer_name': obj.manufacturer_name,
            'manufacturer_address': obj.manufacturer_address,
            'sample_getter1_name': obj.sample_getter1_name,
            'sample_getter1_surname': obj.sample_getter1_surname,
            'sample_getter1_position': obj.sample_getter1_position,
            'sample_getter2_name': obj.sample_getter2_name,
            'sample_getter2_surname': obj.sample_getter2_surname,
            'sample_getter2_position': obj.sample_getter2_position,
            'manufacturer': obj.manufacturer,
            'final_consumer': obj.final_consumer,
            'consumer_name': obj.consumer_name,
            'consumer_address': obj.consumer_address,
            'order_number': obj.order_number,
            'mechanism_name_and_symbol': obj.mechanism_name_and_symbol,
            'sample_delivery': obj.sample_delivery_id,
            'is_OK': obj.is_OK,
            'if_not_why': obj.if_not_why,
            'recipient': obj.recipient,
            'agreement_number': obj.agreement_number,
            'collection_date': obj.collection_date,
            'case_number': obj.case_number,
            'delivery_date': obj.delivery_date,
            'type_of_package': obj.type_of_package,
            'batch_size': obj.batch_size,
            'batch_number': obj.batch_number,
            'batch_production_date': obj.batch_production_date
        }, status=200)

    if request.user.is_authenticated:
        return render(request, 'sample_add.html', contex)
    else:
        return redirect('/')


def sample_menu(request, *args, **kwargs):
    context = {}
    if request.user.is_authenticated:
        return render(request, 'sample_menu.html', context)
    else:
        return redirect('/')


def sample_search(request, *args, **kwargs):

    if request.is_ajax():
        messages.info(request, "Edycja próbki")
        messages.info(request, request.body.decode())
        return JsonResponse({
            'link': "/sample_add/"
        }, status=200)

    if request.user.is_authenticated:
        filters = SampleForm.Meta.labels
        context = {
            "filters": {v: k for v, k in filters.items()},
            "samples": Sampling.objects.select_related('WIJHARS').all()

        }
        return render(request, 'sample_search.html', context)
    else:
        return redirect('/')


def research_add(request, *args, **kwargs):
    contains_error, action, form2, form3, form = add_to_database(request, ResearchForm, FindResearch, Research, 'name')
    contex = {
        "form0": form2,
        "form2": form,
        "form3": form3,
        "action": action
    }

    if request.is_ajax():
        idx = request.body.decode()
        obj = Research.objects.get(id=idx)
        return JsonResponse({
            'sampling': obj.sampling_id,
            'name': obj.name,
            'marking': obj.marking,
            'nutritional_value': obj.nutritional_value,
            'specification': obj.specification,
            'ordinance': obj.ordinance,
            'samples_number': obj.samples_number,
            'result': obj.result,
            'start_date': obj.start_date,
            'research_completion_date': obj.research_completion_date,
            'status': obj.status_id,
            'uncertainty': obj.uncertainty,
            'summary_meet_requirements': obj.summary_meet_requirements,
            'summary_requirements_explains': obj.summary_requirements_explains,
            'requirements': obj.requirements,
            'unit': obj.unit
        }, status=200)
    elif request.user.is_authenticated:
        return render(request, 'research_add.html', contex)
    else:
        return redirect('/')


def additional_data_view(request, *args, **kwargs):
    contex = {}
    if request.user.is_authenticated:
        return render(request, 'additional_forms_mode.html', contex)
    else:
        return redirect('/')


def Control_types_add(request, *args, **kwargs):
    json_response, contex = add_others_to_database(request, ControlTypeForm, FindControlType, ControlType, 'control_type_name')
    if json_response:
        return json_response
    if request.user.is_authenticated:
        return render(request, 'control_type_add.html', contex)
    else:
        return redirect('/')


def Delivery_way_add(request, *args, **kwargs):
    json_response, contex = add_others_to_database(request, DeliveryWayForm, FindDeliveryWays, DeliveryWay, 'delivery_way_name')
    if json_response:
        return json_response
    if request.user.is_authenticated:
        return render(request, 'delivery_way_add.html', contex)
    else:
        return redirect('/')


def Metod_and_norm_add(request, *args, **kwargs):
    json_response, contex = add_others_to_database(request, MetodAndNormForm, FindMetodAndNorms,MetodAndNorm, 'metod_and_norm_name')
    if json_response:
        return json_response
    if request.user.is_authenticated:
        return render(request, 'metod_and_norm_add.html', contex)
    else:
        return redirect('/')


def Research_status_add(request, *args, **kwargs):
    json_response, contex = add_others_to_database(request, ResearchStatusForm, FindResearchStatuses,ResearchStatus, 'research_status_name')
    if json_response:
        return json_response
    if request.user.is_authenticated:
        return render(request,'research_status_add.html', contex)
    else:
        return redirect('/')


def Type_add(request, *args, **kwargs):
    json_response, contex = add_others_to_database(request, TypeForm, FindTypes,Type, 'type_name')
    if json_response:
        return json_response
    if request.user.is_authenticated:
        return render(request, 'type_add.html', contex)
    else:
        return redirect('/')


def Wijhars_add(request, *args, **kwargs):
    json_response, contex = add_others_to_database(request, WIJHARSForm, FindWIJHARSs,WIJHARS, 'wijhars_name')
    if json_response:
        return json_response
    if request.user.is_authenticated:
        return render(request, 'wijhars_add.html', contex)
    else:
        return redirect('/')

