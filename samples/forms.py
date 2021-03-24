from django.utils.translation import gettext_lazy as _
from .models import FormPart1, FormPart2
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = ('%Y-%m-%d')


class SampleForm(forms.ModelForm):
    class Meta:
        model = FormPart1
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


class FormPart2(forms.ModelForm):
    class Meta:
        model = FormPart2
        fields = ('manufacturer_name', 'manufacturer_address','sample_getter1_name','sample_getter1_surname','sample_getter1_position','sample_getter2_name','sample_getter2_surname',
                  'sample_getter2_position','manufacturer','final_consumer','consumer_name','consumer_address','order_number','mechanism_name_and_symbol','sample_delivery')
        labels = {
            'manufacturer_name': _('nazwa'),
            'manufacturer_address': _('adres'),
            'sample_getter1_name': _('imię'),
            'sample_getter1_surname': _('nazwisko'),
            'sample_getter1_position': _('stanowisko'),
            'sample_getter2_name': _('imię'),
            'sample_getter2_surname': _('nazwisko'),
            'sample_getter2_position': _('stanowisko'),
            'manufacturer': _('producent (nazwa i adres)'),
            'final_consumer': _('konsument finalny'),
            'consumer_name': _('nazwa'),
            'consumer_address': _('address'),
            'order_number': _('numer zlecenia'),
            'mechanism_name_and_symbol': _('nazwa i symbol mechanizmu'),
            'sample_delivery': _('sposób dostarczenia próbki')
        }
