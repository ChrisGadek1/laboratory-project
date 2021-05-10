from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from django.contrib.auth import password_validation
# Create your views here.


def password_change_view(request, *args, **kwargs):
    username = Account.get_username(request.user)
    list = []
    error_message = {'error' : list}

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password_1')
        confirmation_password = request.POST.get('new_password_2')

        if request.user.check_password(old_password):
            if new_password == confirmation_password:
                try:
                    password_validation.validate_password(new_password)
                    request.user.set_password(new_password)
                    request.user.must_change_password = False
                    request.user.save()
                    return redirect('/', messages.add_message(request, messages.INFO, 'Poprawnie zakończony proces zmiany hasła. Zaloguj się do systemu za pomocą nowego hasła'))
                except password_validation.ValidationError as errors:
                    list.append("Podane hasło nie spełnia wymagań bezpieczeństwa. Spróbuj ponownie wypełnić formularz")
                    if any('This password is too short' for _ in errors):
                        list.append("Twoje hasło musi zawierać conajmniej 8 liter")
                    if 'This password is too common.' in errors:
                        list.append("Twoje hasło nie może być powszechnie używanym hasłem")
                    if 'This password is entirely numeric.' in errors:
                        list.append("Twoje hasło nie może składać się wyłącznie z cyfr")
                    if any('password_too_similar' for _ in errors):
                        list.append("Twoje hasło nie może być podobne do twoich prywatnych danych")
            else:
               list.append("Podane nowe hasło i jego potwierdzenie nie zgadzają się. Spróbuj ponownie wypełnić formularz")
        else:
            list.append("Podane dotychczasowe hasło jest błędne. Spróbuj ponownie wypełnić formularz")

    if request.user.is_authenticated:
        return render(request, 'change_password.html', error_message)
    else:
        return redirect('/')