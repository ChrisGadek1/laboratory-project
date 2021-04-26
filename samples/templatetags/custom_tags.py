from django import template
from django.core import serializers

register = template.Library()


def get_prop_value(value, arg):
    return getattr(value, arg)


@register.filter
def get_fields(obj):
    return obj._meta.get_fields()


@register.filter(is_safe=True)
def js(obj):
    return serializers.serialize('json', obj)

register.filter('get_prop_value', get_prop_value)