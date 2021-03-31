from django.utils.translation import gettext_lazy as _
from .models import Sampling, Research
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = ('%Y-%m-%d')


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sampling
        fields = ('number','code','WIJHARS','assortment','admission_date','completion_date', 'expiration_date','additional_comment',
                  'customer_name','size','condition','appeal_analysis','control_type','type','sampling_method',
                  'manufacturer_name', 'manufacturer_address', 'sample_getter1_name', 'sample_getter1_surname',
                  'sample_getter1_position', 'sample_getter2_name', 'sample_getter2_surname',
                  'sample_getter2_position', 'manufacturer', 'final_consumer', 'consumer_name', 'consumer_address',
                  'order_number', 'mechanism_name_and_symbol', 'sample_delivery')
        labels = {
            'number': _('Numer próbki'),
            'code': _('Kod próbki'),
            'WIJHARS': _('WIJHARS'),
            'assortment': _('Asortyment'),
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
            'manufacturer_name': _('Nazwa'),
            'manufacturer_address': _('Adres'),
            'sample_getter1_name': _('Imię'),
            'sample_getter1_surname': _('Nazwisko'),
            'sample_getter1_position': _('Stanowisko'),
            'sample_getter2_name': _('Imię'),
            'sample_getter2_surname': _('Nazwisko'),
            'sample_getter2_position': _('Stanowisko'),
            'manufacturer': _('Producent (nazwa i adres)'),
            'final_consumer': _('Konsument finalny'),
            'consumer_name': _('Nazwa'),
            'consumer_address': _('Address'),
            'order_number': _('Numer zlecenia'),
            'mechanism_name_and_symbol': _('Nazwa i symbol mechanizmu'),
            'sample_delivery': _('Sposób dostarczenia próbki')
        }
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'test placeholdera'}),
            'admission_date' : DateInput,
            'expiration_date' : DateInput,
            'completion_date' : DateInput,
        }


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ('sampling','name', 'marking','nutritional_value','specification','ordinance','samples_number','result',
                  'start_date','completion_date','status','uncertainty','summary_meet_requirements', 'summary_requirements_explains')
        labels = {
            'sampling': _('Numer próbki'),
            'name': _('Nazwa'),
            'marking': _('Oznakowanie'),
            'nutritional_value': _('Wartość odżywcza'),
            'specification': _('Specyfikacja'),
            'ordinance': _('Rozporządzenie'),
            'samples_number': _('Liczba próbek do badania'),
            'result': _('Wynik badania'),
            'start_date': _('Data rozpoczęcia'),
            'completion_date': _('Data zakończenia'),
            'status': _('Status metody'),
            'uncertainty': _('Niepewność, LOD, LOQ'),
            'summary_meet_requirements': _('Czy próbka spełnia wymagania?'),
            'summary_requirements_explains': _('Jeżeli nie spełnia, dlaczego')
        }