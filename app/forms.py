from django.utils.translation import gettext_lazy as _
from django import forms


class RawLoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

