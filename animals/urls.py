# animals/urls.py
from django.urls import path
from .views import animal_list,country_list,home

urlpatterns = [
    path('', home, name='home'),
    path('animals/', animal_list, name='animal_list'),
    path('countries/', country_list, name='country_list'),
]