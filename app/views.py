from django.shortcuts import render

# Create your views here.


def main_site(request, *args, **kwargs):
    return render(request, 'main_logged.html', {})

