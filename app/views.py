from django.shortcuts import render
# Create your views here.


def main_site(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'main_logged.html', {})
    else:
        return render(request, 'main_not_logged.html', {})
