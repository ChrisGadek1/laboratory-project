from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RawLoginForm

# Create your views here.


def main_view(request):
    return render(request, 'basic.html')


def main_site(request):
    return render(request, 'main.html')
