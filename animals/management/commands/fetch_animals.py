# animals/management/commands/fetch_animals_wiki.py
import wikipedia
import requests
from django.core.management.base import BaseCommand
from animals.models import Animal

# class Command(BaseCommand):
#     help = 'Fetch animal data from Wikipedia'

#     def handle(self, *args, **options):
#         animal_wikidata_id = ["Q81214","Q140","Q186778","Q998685","Q190154","Q113297","Q179020","Q4504","Q41181","Q136842","Q402885","Q844643","Q30197","Q1750802"]
#         for wikidata_id in animal_wikidata_id:
#             try:
#                 print(wikidata_id)
#                 wikipedia.set_lang("en")
#                 image_url = ""
#                 url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
#                 data = requests.get(url).json()
#                 sitelinks = data['entities'][wikidata_id]['sitelinks']
#                 claims = data['entities'][wikidata_id]['claims']
#                 title = sitelinks.get("enwiki", {}).get("title")
#                 french_name = sitelinks.get("frwiki", {}).get("title")
#                 print("Wikipedia title:", title)
#                 image = ""
#                 if "P18" in claims:
#                     image = claims["P18"][0]["mainsnak"]["datavalue"]["value"]
#                     #print("Image file name:", image)
#                     image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image}"
#                     #print("Image URL:", image_url)

#                     # Optional: test if image exists
#                     res = requests.get(image_url)
#                     #print("Image request status:", res.status_code)
#                 else:
#                     print("No image (P18) found.")      
#                 Animal.objects.update_or_create(
#                     name=title,
#                     french_name=french_name,
#                     defaults={"summary": "", "image_url": image_url}
#                 )
#                 self.stdout.write(self.style.SUCCESS(f"Fetched: {title}"))
#             except Exception as e:
#                 self.stderr.write(f"Failed for {title}: {e}")


class Command(BaseCommand):
    help = "Fetch animals using Wikidata Q-IDs and save them"

    def handle(self, *args, **options):
        wikidata_ids = ["Q81214","Q140","Q186778","Q998685","Q190154","Q113297","Q179020","Q4504","Q41181","Q136842","Q402885","Q844643","Q30197","Q1750802", "Q7378","Q2191516"] 
        Animal.objects.all().delete()  # clear existing data
        for wikidata_id in wikidata_ids:
            try:
                entity_url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
                entity_data = requests.get(entity_url).json()
                entity = entity_data['entities'][wikidata_id]
                labels = entity.get("labels", {})
                claims = entity.get("claims", {})
                sitelinks = entity.get("sitelinks", {})

                # Common name (English label)
                name = labels.get("en", {}).get("value", f"Unknown-{wikidata_id}")

                french_name = labels.get("fr", {}).get("value", f"Unknown-{wikidata_id}")

                # Scientific name (P225)
                scientific_name = ""
                if "P225" in claims:
                    scientific_name = claims["P225"][0]["mainsnak"]["datavalue"]["value"]

                # Image file name (P18)
                image_url = ""
                if "P18" in claims:
                    image_file = claims["P18"][0]["mainsnak"]["datavalue"]["value"]
                    image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image_file}"

                # Wikipedia title
                wikipedia_title = sitelinks.get("enwiki", {}).get("title", "")

                # Wikipedia summary
                summary = ""
                if wikipedia_title:
                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wikipedia_title}"
                    res = requests.get(summary_url)
                    if res.status_code == 200:
                        summary = res.json().get("extract", "")

                # Save or update the Animal object
                Animal.objects.update_or_create(
                    wikidata_id=wikidata_id,
                    defaults={
                        "name": name,
                        "french_name" :french_name,
                        "scientific_name": scientific_name,
                        "image_url": image_url,
                        "wikipedia_title": wikipedia_title,
                        "summary": summary
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Saved {name} ({wikidata_id})"))

            except Exception as e:
                self.stderr.write(f"Error processing {wikidata_id}: {e}")