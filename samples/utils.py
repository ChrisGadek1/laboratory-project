from .forms import ChoiceAction
from django.contrib import messages
from django.http import JsonResponse


def add_to_database(request, object_form, object_form_3, object_class, field_name):
    form2 = ChoiceAction(request.POST)
    form3 = object_form_3(request.POST)
    form = object_form(data=request.POST, mode=form2["mode_name"].value())

    contains_error = False
    action = 'None'
    obj = None
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    if field_name == 'number':
                        obj = object_class.objects.get(number=form[field_name].value())
                    else:
                        obj = object_class.objects.get(name=form[field_name].value())
                    form = object_form(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    if field_name == 'number':
                        obj = object_class.objects.get(number=form[field_name].value())
                    else:
                        obj = object_class.objects.get(name=form[field_name].value())
                    obj.delete()
                    action = "Delete"
            else:
                messages.error(request, form.errors)
                contains_error = True
    return contains_error, action, form2, form3, form


def add_others_to_database(request, object_form, object_form_3, object_class, field_name):
    contains_error = False
    form2 = ChoiceAction(request.POST)
    form = object_form(data=request.POST, mode=form2["mode_name"].value())
    form3 = object_form_3(request.POST)
    action = 'None'
    if not request.is_ajax():
        if request.method == 'POST':
            if form.is_valid():
                if form2['mode_name'].value() == "Add":
                    form.save()
                    action = "Add"
                elif form2['mode_name'].value() == "Edit":
                    obj = object_class.objects.get(id=form3[field_name].value())
                    form = object_form(data=request.POST, mode=form2["mode_name"].value(), instance=obj)
                    form.save()
                    action = "Edit"
                else:
                    obj = object_class.objects.get(id=form3[field_name].value())
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
        obj = object_class.objects.get(id=idx)
        return JsonResponse({
            'name': obj.name,
        }, status=200), None
    return None, contex