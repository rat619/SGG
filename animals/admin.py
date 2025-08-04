from django.contrib import admin
from .models import Animal,Country

admin.site.site_header = "Family Guessing games"
admin.site.site_title = "Family Guessing games"
admin.site.index_title = "Welcome to administration"

    
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'wikipedia_title','french_name','scientific_name')  



@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'wikipedia_title','french_name','scientific_name') 

# Register your models here.
