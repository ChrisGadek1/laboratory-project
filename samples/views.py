from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import SampleForm, ResearchForm, ChoiceAction
from .models import Sampling, Research

# Create your views here.


def main_site(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'main_logged.html', {})
    else:
        return render(request, 'main_not_logged.html', {})


def sample_add(request, *args, **kwargs):
    form = SampleForm(request.POST)
    form2 = ChoiceAction(request.POST)
    form3 = ResearchForm(request.POST)

    if not request.is_ajax():
        if form.is_valid():
            if form2['mode_name'].value() == "Add":
                form.save()
            elif form2['mode_name'].value() == "Edit":
                obj = Sampling.objects.get(id=form3['sampling'].value())
                form = SampleForm(request.POST, instance=obj)
                form.save()
            else:
                obj = Sampling.objects.get(id=form3['sampling'].value())
                obj.delete()

    contex = {
        "form0" : ChoiceAction,
        "form1" : SampleForm,
        "form2": ResearchForm,
    }

    if request.is_ajax():
        idx = request.body.decode()
        print(idx)
        obj = Sampling.objects.get(id=idx)
        print(obj.number)
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
        }, status=200)
    elif request.user.is_authenticated:
        return render(request, 'sample_add.html', contex)
    else:
        return redirect('/')


def research_add(request, *args, **kwargs):

    form = ResearchForm(request.POST or None)
    form2 = ChoiceAction(request.POST)

    print(request.POST)
    if not request.is_ajax():
        if form.is_valid():
            if form2['mode_name'].value() == "Add":
                form.save()
            elif form2['mode_name'].value() == "Edit":
                obj = Research.objects.get(name=request.POST['name_searching'])
                form = ResearchForm(request.POST, instance=obj)
                form.save()
            else:
                obj = Research.objects.get(name=form['name_searching'])
                obj.delete()

    contex = {
        "form0": ChoiceAction,
        "form2": ResearchForm,
    }

    if request.is_ajax():
        idx = request.body.decode()
        obj = Research.objects.get(name=idx)
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
            'completion_date': obj.completion_date,
            'status': obj.status_id,
            'uncertainty': obj.uncertainty,
            'summary_meet_requirements': obj.summary_meet_requirements,
            'summary_requirements_explains': obj.summary_requirements_explains
        }, status=200)
    elif request.user.is_authenticated:
        return render(request, 'research_add.html', contex)
    else:
        return redirect('/')