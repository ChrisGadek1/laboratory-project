from django.utils.translation import gettext_lazy as _
from .models import CsvOptions
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = ('%Y-%m-%d')


class CsvOptionsAction(forms.ModelForm):
    class Meta:
        model = CsvOptions
        fields = '__all__'
        labels = {
            'option': _('Którą rzecz chcesz pobrać z/dodać do bazy danych ?'),
            'mode': _('Wybierz opcje'),
        }