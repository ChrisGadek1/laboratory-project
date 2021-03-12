from django.contrib.auth import get_user_model
from django.shortcuts import render
from .forms import RawLoginForm

# Create your views here.

def main_view(request):
    return render(request, 'basic.html')


def login_view(request):
    login_form = RawLoginForm()
    if request.method == "POST":
        login_form = RawLoginForm(request.POST)

        if login_form.is_valid():
            print("asdsad")
        else:
            print("ułała")

    context = {
        "form": login_form
    }

    return render(request, 'login.html', context)


def main_site(request):
    return render(request, 'main.html')
