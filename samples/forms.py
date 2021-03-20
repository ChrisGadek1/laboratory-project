from django.utils.translation import gettext_lazy as _
from .models import Sample
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = ('%Y-%m-%d')


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ('number','code','WIJHARS','assortment','admission_date','completion_date', 'expiration_date','additional_comment',
                  'customer_name','size','condition','appeal_analysis','control_type','type','sampling_method')
        labels = {
            'number': _('numer próbki'),
            'code': _('Kod próbki'),
            'WIJHARS': _('WIJHARS'),
            'assortment': _('Data przyjęcia próbki'),
            'admission_date': _('Data przydatności'),
            'completion_date': _('Data zakończenia badań'),
            'expiration_date': _('Data przydatności badań'),
            'additional_comment': _('Dodatkowy komenatarz'),
            'customer_name': _('Nazwa klienta'),
            'size': _('Wielkość próbki'),
            'condition': _('Stan próbki '),
            'appeal_analysis': _('Analiza odwoławcza'),
            'control_type': _('Rodzaj kontroli '),
            'type': _('Rodzaj próbki'),
            'sampling_method': _('Metoda/Norma pobrania próbki'),
        }
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'test placeholdera'}),
            'admission_date' : DateInput,
            'expiration_date' : DateInput,
            'completion_date' : DateInput,
        }