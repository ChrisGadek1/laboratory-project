"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from app.views import main_site
from reports.views import choose_mode, add_template, generate_report
from samples.views import sample_add, research_add
from csvs.views import generate_csv, choose_mode_csv, read_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_site),
    path('accounts/', include("django.contrib.auth.urls")),
    path('sample_add/', sample_add),
    path('research_add/', research_add),
    path('choose_mode/', choose_mode),
    path('choose_mode/add_template', add_template),
    path('choose_mode/generate_report/', generate_report),
    path('choose_mode_csv/', choose_mode_csv),
    path('choose_mode_csv/csv/', generate_csv),
    path('choose_mode_csv/read_csv/', read_csv)
]
