from django.shortcuts import render
from .models import Animal, Country

def home(request):
    return render(request, "animals/home.html")

def animal_list(request):
    animals = Animal.objects.all()
    return render(request, "animals/animal_list.html", {"animals": animals})

def country_list(request):
    countries = Country.objects.all()
    return render(request, "animals/country_list.html", {"countries": countries})
