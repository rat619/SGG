# animals/urls.py
from django.urls import path
from .views import animal_list,country_list,home,guess_view_animal,guess_view_country

urlpatterns = [
    path('', home, name='home'),
    path('animals/', animal_list, name='animal_list'),
    path('countries/', country_list, name='country_list'),
    path("guess_animal/", guess_view_animal, name="guess_animal"),
    path("guess_country/", guess_view_country, name="guess_country"),
]