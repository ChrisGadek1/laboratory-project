from django.utils.translation import gettext_lazy as _
from .models import Sampling, Research, Mode
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = ('%Y-%m-%d')


class ChoiceAction(forms.ModelForm):
    class Meta:
        model = Mode
        fields = ('mode_name',)
        labels = {
            'mode_name': _('Co chcesz zrobić z próbką'),
        }


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sampling
        fields = ('__all__')
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
            'sample_delivery': _('Sposób dostarczenia próbki'),
            'is_OK': _('Czy próbka spełnia wymagania?'),
            'if_not_why': _('Jeżeli nie, dlaczego')
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
        fields = ('__all__')
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

        widgets = {
            'start_date': DateInput,
            'completion_date': DateInput,
        }