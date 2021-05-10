from django.utils.translation import gettext_lazy as _
from .models import Sampling, Research, Mode, FindResearch, ControlType, FindControlType, \
    DeliveryWay, FindDeliveryWay, WIJHARS, FindWIJHARS, Type, FindType, ResearchStatus, FindResearchStatus, \
    MetodAndNorm, FindMetodAndNorm

from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = ('%Y-%m-%d')


class ChoiceAction(forms.ModelForm):
    class Meta:
        model = Mode
        fields = ('mode_name',)
        labels = {
            'mode_name': _('Tryb formularza'),
        }


class ControlTypeForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(ControlTypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ControlType
        fields = '__all__'
        labels = {
            'name': _('nazwa'),
        }


class FindControlType(forms.ModelForm):
    class Meta:
        model = FindControlType
        fields = '__all__'
        labels = {
            'control_type_name': _('Wybierz typ kontroli')
        }


class SampleForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(SampleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sampling
        fields = '__all__'
        labels = {
            'number': _('Numer próbki'),
            'code': _('Kod próbki'),
            'WIJHARS': _('WIJHARS'),
            'assortment': _('Asortyment'),
            'admission_date': _('Data przydatności'),
            'completion_date': _('Data zakończenia badań'),
            'expiration_date': _('Data przydatności badań'),
            'additional_comment': _('Dodatkowy komenatarz do dat'),
            'customer_name': _('Nazwa klienta'),
            'size': _('Wielkość próbki'),
            'condition': _('Stan próbki '),
            'appeal_analysis': _('Analiza odwoławcza'),
            'control_type': _('Rodzaj kontroli '),
            'type': _('Rodzaj próbki'),
            'sampling_method': _('Metoda/Norma pobrania próbki'),
            'manufacturer_name': _('Nazwa producenta'),
            'manufacturer_address': _('Adres producenta'),
            'sample_getter1_name': _('Imię pobierającego nr 1'),
            'sample_getter1_surname': _('Nazwisko pobierającego nr 1'),
            'sample_getter1_position': _('Stanowisko pobierającego nr 1'),
            'sample_getter2_name': _('Imię pobierającego nr 2'),
            'sample_getter2_surname': _('Nazwisko pobierającego nr 2'),
            'sample_getter2_position': _('Stanowisko pobierającego nr 2'),
            'manufacturer': _('Producent (nazwa i adres)'),
            'final_consumer': _('Konsument finalny'),
            'consumer_name': _('Nazwa Klienta'),
            'consumer_address': _('Address Klienta'),
            'order_number': _('Numer zlecenia'),
            'mechanism_name_and_symbol': _('Nazwa i symbol mechanizmu'),
            'sample_delivery': _('Sposób dostarczenia próbki'),
            'is_OK': _('Czy próbka spełnia wymagania?'),
            'if_not_why': _('Jeżeli nie spełnia, dlaczego'),
            'recipient': _('Odbiorca'),
            'agreement_number': _('Nr Zlecenia/Umowy'),
            'collection_date': _('Data pobrania próbki'),
            'case_number': _('Numer sprawy'),
            'delivery_date': _('Data dostarczenia do laboratorium'),
            'type_of_package': _('Rodzaj opakowania jednostkowego'),
            'batch_size': _('Wielkość Partii'),
            'batch_number': _('Numer Partii'),
            'batch_production_date': _('Data produkcji')
        }
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'kod próbki'}),
            'admission_date': DateInput,
            'expiration_date': DateInput,
            'completion_date': DateInput,
            'batch_production_date': DateInput,
            'collection_date': DateInput,
            'delivery_date': DateInput
        }

    def clean_number(self, *args, **kwargs):
        if self.mode != "Add" and Sampling.objects.filter(number=self.cleaned_data.get("number")).count() == 0:
            raise forms.ValidationError("nie istnieje próka o podanym numerze")
        elif self.mode == "Add" and Sampling.objects.filter(number=self.cleaned_data.get("number")).count() > 0:
            raise forms.ValidationError("istnieje już próbka o podanym numerze")
        else:
            return self.cleaned_data.get("number")

    def clean_code(self, *args, **kwargs):
        if self.mode != "Add" and Sampling.objects.filter(code=self.cleaned_data.get("code")).count() == 0:
            raise forms.ValidationError("nie istnieje próka o podanym kodzie")
        elif self.mode == "Add" and Sampling.objects.filter(code=self.cleaned_data.get("code")).count() > 0:
            raise forms.ValidationError("istnieje już próbka o podanym kodzie")
        else:
            return self.cleaned_data.get("code")


class FindResearch(forms.ModelForm):
    class Meta:
        model = FindResearch
        fields = '__all__'
        labels = {
            'research_name': _('Wybierz badanie')
        }


class ResearchForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(ResearchForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Research
        fields = ('__all__')
        labels = {
            'sampling': _('Kod próbki'),
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
            'summary_requirements_explains': _('Jeżeli nie spełnia, dlaczego'),
            'requirements': _('Wymagania wg'),
            'unit': _('Jednostka')
        }

        widgets = {
            'start_date': DateInput,
            'completion_date': DateInput,
        }

    def clean_name(self, *args, **kwargs):
        if self.mode == "Add" and Research.objects.filter(name=self.cleaned_data.get("name")).count() > 0:
            raise forms.ValidationError("istnieje już badanie o podanej nazwie")
        elif self.mode != "Add" and Research.objects.filter(name=self.cleaned_data.get("name")).count() == 0:
            raise forms.ValidationError("nie istnieje badanie o podanej nazwie")
        else:
            return self.cleaned_data.get("name")


class DeliveryWayForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(DeliveryWayForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DeliveryWay
        fields = '__all__'
        labels = {
            'name': _('nazwa'),
        }


class FindDeliveryWays(forms.ModelForm):
    class Meta:
        model = FindDeliveryWay
        fields = '__all__'
        labels = {
            'delivery_way_name': _('Wybierz sposób dostarczania')
        }


class WIJHARSForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(WIJHARSForm, self).__init__(*args, **kwargs)

    class Meta:
        model = WIJHARS
        fields = '__all__'
        labels = {
            'name': _('nazwa'),
        }


class FindWIJHARSs(forms.ModelForm):
    class Meta:
        model = FindWIJHARS
        fields = '__all__'
        labels = {
            'wijhars_name': _('Wybierz WIJHARS')
        }


class TypeForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(TypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Type
        fields = '__all__'
        labels = {
            'name': _('nazwa'),
        }


class FindTypes(forms.ModelForm):
    class Meta:
        model = FindType
        fields = '__all__'
        labels = {
            'type_name': _('Wybierz typ badania')
        }


class ResearchStatusForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(ResearchStatusForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ResearchStatus
        fields = '__all__'
        labels = {
            'name': _('nazwa'),
        }


class FindResearchStatuses(forms.ModelForm):
    class Meta:
        model = FindResearchStatus
        fields = '__all__'
        labels = {
            'research_status_name': _('Wybierz status badań')
        }


class MetodAndNormForm(forms.ModelForm):
    def __init__(self, mode, *args, **kwargs):
        self.mode = mode
        super(MetodAndNormForm, self).__init__(*args, **kwargs)

    class Meta:
        model = MetodAndNorm
        fields = '__all__'
        labels = {
            'name': _('nazwa'),
        }


class FindMetodAndNorms(forms.ModelForm):
    class Meta:
        model = FindMetodAndNorm
        fields = '__all__'
        labels = {
            'metod_and_norm_name': _('Wybierz metode/norme badania')
        }