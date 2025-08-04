from django.db import models

# class Animal(models.Model):
#     name = models.CharField(max_length=200)
#     french_name = models.CharField(max_length=200,blank=True)    
#     summary = models.TextField(blank=True)
#     image_url = models.URLField(blank=True)

#     def __str__(self):
#          return self.name


class Animal(models.Model):
    name = models.CharField(max_length=255)  # Common name (e.g., Lion)
    french_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    wikipedia_title = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    wikidata_id = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animals"

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=255)  # Common name (e.g., Lion)
    french_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    wikipedia_title = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    wikidata_id = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name