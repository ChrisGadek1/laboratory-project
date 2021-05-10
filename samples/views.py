from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import SampleForm, ResearchForm, ChoiceAction, FindResearch, ControlTypeForm, FindControlType,\
    DeliveryWayForm, FindDeliveryWays, WIJHARSForm, FindWIJHARSs, TypeForm, FindTypes, ResearchStatusForm, FindResearchStatuses, \
    MetodAndNormForm, FindMetodAndNorms
from .models import Sampling, Research, ControlType, DeliveryWay, WIJHARS, Type, ResearchStatus, MetodAndNorm
from django.contrib import messages


# Create your views here.


def main_site(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'main_logged.html', {})
    else:
        return render(request, 'main_not_logged.html', {})


def sample_add(request, *args, **kwargs):
    form2 = ChoiceAction(request.POST)
    form3 = ResearchForm(request.POST)
    form = SampleForm(data=request.POST, mode=form2["mode_name"].value())

    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = Sampling.objects.get(number=form['number'].value())
                    form = SampleForm(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = Sampling.objects.get(number=form['number'].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action
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
    form2 = ChoiceAction(request.POST)
    form3 = FindResearch(request.POST)
    form = ResearchForm(data=request.POST, mode=form2["mode_name"].value())

    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = 'Add'
                elif form2['mode_name'].value() == "Edit":
                    obj = Research.objects.get(name=form["name"].value())
                    form = ResearchForm(mode=form2["mode_name"].value(), data=request.POST, instance=obj)
                    form.save()
                    action = 'Edit'
                else:
                    obj = Research.objects.get(name=form["name"].value())
                    obj.delete()
                    action = 'Delete'
            else:
                messages.error(request, form.errors)

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
    form2 = ChoiceAction(request.POST)
    form = ControlTypeForm(data=request.POST, mode=form2["mode_name"].value())
    form3 = FindControlType(request.POST)
    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = ControlType.objects.get(id=form3['control_type_name'].value())
                    form = ControlTypeForm(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = ControlType.objects.get(id=form3['control_type_name'].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action
    }
    if request.is_ajax():
        idx = request.body.decode()
        obj = ControlType.objects.get(id=idx)
        return JsonResponse({
            'name': obj.name,
        }, status=200)
    if request.user.is_authenticated:
        return render(request, 'control_type_add.html', contex)
    else:
        return redirect('/')


def Delivery_way_add(request, *args, **kwargs):
    form2 = ChoiceAction(request.POST)
    form = DeliveryWayForm(data=request.POST, mode=form2["mode_name"].value())
    form3 = FindDeliveryWays(request.POST)
    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = DeliveryWay.objects.get(id=form3['delivery_way_name'].value())
                    form = DeliveryWayForm(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = DeliveryWay.objects.get(id=form3['delivery_way_name'].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action
    }
    if request.is_ajax():
        idx = request.body.decode()
        obj = DeliveryWay.objects.get(id=idx)
        return JsonResponse({
            'name': obj.name,
        }, status=200)
    if request.user.is_authenticated:
        return render(request, 'delivery_way_add.html', contex)
    else:
        return redirect('/')


def Metod_and_norm_add(request, *args, **kwargs):
    form2 = ChoiceAction(request.POST)
    form = MetodAndNormForm(data=request.POST, mode=form2["mode_name"].value())
    form3 = FindMetodAndNorms(request.POST)
    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = MetodAndNorm.objects.get(id=form3['metod_and_norm_name'].value())
                    form = MetodAndNormForm(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = MetodAndNorm.objects.get(id=form3['metod_and_norm_name'].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action
    }
    if request.is_ajax():
        idx = request.body.decode()
        obj = MetodAndNorm.objects.get(id=idx)
        return JsonResponse({
            'name': obj.name,
        }, status=200)
    if request.user.is_authenticated:
        return render(request, 'metod_and_norm_add.html', contex)
    else:
        return redirect('/')


def Research_status_add(request, *args, **kwargs):
    form2 = ChoiceAction(request.POST)
    form = ResearchStatusForm(data=request.POST, mode=form2["mode_name"].value())
    form3 = FindResearchStatuses(request.POST)
    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = ResearchStatus.objects.get(id=form3['research_status_name'].value())
                    form = ResearchStatusForm(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = ResearchStatus.objects.get(id=form3['research_status_name'].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action
    }
    if request.is_ajax():
        idx = request.body.decode()
        obj = ResearchStatus.objects.get(id=idx)
        return JsonResponse({
            'name': obj.name,
        }, status=200)
    if request.user.is_authenticated:
        return render(request,'research_status_add.html', contex)
    else:
        return redirect('/')


def Type_add(request, *args, **kwargs):
    form2 = ChoiceAction(request.POST)
    form = TypeForm(data=request.POST, mode=form2["mode_name"].value())
    form3 = FindTypes(request.POST)
    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = Type.objects.get(id=form3['type_name'].value())
                    form = TypeForm(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = Type.objects.get(id=form3['type_name'].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action
    }
    if request.is_ajax():
        idx = request.body.decode()
        obj = Type.objects.get(id=idx)
        return JsonResponse({
            'name': obj.name,
        }, status=200)
    if request.user.is_authenticated:
        return render(request, 'type_add.html', contex)
    else:
        return redirect('/')


def Wijhars_add(request, *args, **kwargs):
    form2 = ChoiceAction(request.POST)
    form = WIJHARSForm(data=request.POST, mode=form2["mode_name"].value())
    form3 = FindWIJHARSs(request.POST)
    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = WIJHARS.objects.get(id=form3['wijhars_name'].value())
                    form = WIJHARSForm(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = WIJHARS.objects.get(id=form3['wijhars_name'].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)

    contex = {
        "form0": form2,
        "form1": form,
        "form2": form3,
        "action": action
    }
    if request.is_ajax():
        idx = request.body.decode()
        obj = WIJHARS.objects.get(id=idx)
        return JsonResponse({
            'name': obj.name,
        }, status=200)
    if request.user.is_authenticated:
        return render(request, 'wijhars_add.html', contex)
    else:
        return redirect('/')

