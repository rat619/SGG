import random
from django.shortcuts import render, redirect
from .models import Animal, Country

def home(request):
    return render(request, "animals/home.html")

def animal_list(request):
    animals = Animal.objects.all()
    return render(request, "animals/animal_list.html", {"animals": animals})

def country_list(request):
    countries = Country.objects.all()
    return render(request, "animals/country_list.html", {"countries": countries})


def guess_view_animal(request):
    # Select a random animal
    animals = Animal.objects.all()
    if not animals.exists():
        return render(request, "animals/guess_animal.html", {"error": "No animals in the database."})
    
    if request.GET.get("next") == "1" and request.method != "POST":
        print('test')
        request.session.pop("guess_animal_id", None)

    # Store the correct answer in session if not already there
    if "guess_animal_id" not in request.session:
        print("test 2")
        selected = random.choice(animals)
        request.session["guess_animal_id"] = selected.id
    else:
        selected = Animal.objects.get(id=request.session["guess_animal_id"])

    message = ""
    correct = None
    user_guess = ''
   # previous_guess = request.session.get("last_guess", "")
    # If the user submitted a guess
    if request.method == "POST":   
        user_guess = request.POST.get("guess", "").strip().lower()
        print(user_guess)
        print(selected.french_name.lower())
        print(selected.french_name.lower() in user_guess.lower())
        if (user_guess) and user_guess.lower() in selected.french_name.lower():
            message = f"✅ Correct! It was {selected.french_name}."
            correct = True
            del request.session["guess_animal_id"]
        else:
            message = "❌ Wrong guess! Try again."
            correct = False

    return render(request, "animals/guess_animal.html", {
        "last_guess": request.POST.get("guess", ""),
        "animal": selected,
        "message": message,
        "correct": correct,
    })



def guess_view_country(request):
     # Select a random animal
    countries = Country.objects.all()
    if not countries.exists():
        return render(request, "animals/guess_country.html", {"error": "No countries in the database."})
    
    if request.GET.get("next") == "1" and request.method != "POST":
        request.session.pop("guess_country_id", None)

    # Store the correct answer in session if not already there
    if "guess_country_id" not in request.session:
        selected = random.choice(countries)
        request.session["guess_country_id"] = selected.id
    else:
        selected = Country.objects.get(id=request.session["guess_country_id"])

    message = ""
    correct = None
    user_guess = ''
   # previous_guess = request.session.get("last_guess", "")
    # If the user submitted a guess
    if request.method == "POST":   
        user_guess = request.POST.get("guess", "").strip().lower()
        if (user_guess) and user_guess.lower() in selected.french_name.lower():
            message = f"✅ Correct! It was {selected.french_name}."
            correct = True
            del request.session["guess_country_id"]
        else:
            message = "❌ Wrong guess! Try again."
            correct = False

    return render(request, "animals/guess_country.html", {
        "last_guess": request.POST.get("guess", ""),
        "country": selected,
        "message": message,
        "correct": correct,
    })


