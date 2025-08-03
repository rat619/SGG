import requests
from django.core.management.base import BaseCommand
from animals.models import Country

def get_flag_image_from_claims(claims):
    if "P41" not in claims:
        return None

    # Filter out deprecated ranks
    valid_flags = [
        claim for claim in claims["P41"]
        if claim.get("rank") in ["normal", "preferred"]
    ]

    if not valid_flags:
        return None

    # Optionally sort by start time (P580)
    def get_start_time(claim):
        try:
            return claim['qualifiers']['P580'][0]['datavalue']['value']['time']
        except:
            return ''  # Fallback if no date

    # Sort flags by start time descending, newest first
    valid_flags.sort(key=get_start_time, reverse=True)

    # Get the image file name from the most relevant claim
    image_file = valid_flags[0]['mainsnak']['datavalue']['value']
    image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image_file}"
    return image_url

def get_capital_label(claims):
    if "P36" not in claims:
        return None

    capital_id = claims["P36"][0]["mainsnak"]["datavalue"]["value"]["id"]

    # Fetch capital entity to get its English label
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{capital_id}.json"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        label = data["entities"][capital_id]["labels"].get("en", {}).get("value")
        return label
    return None

class Command(BaseCommand):
    help = "Fetch animals using Wikidata Q-IDs and save them"

    def handle(self, *args, **options):
        wikidata_ids = ["Q1019","Q142","Q29","Q159"] 
        Country.objects.all().delete()  # clear existing data
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

                capital = get_capital_label(claims)

                # Image file name (P18)
                image_url = ""
                image_url = get_flag_image_from_claims(claims)

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
                Country.objects.update_or_create(
                    wikidata_id=wikidata_id,
                    defaults={
                        "name": name,
                        "french_name" :french_name,
                        "scientific_name": capital,
                        "image_url": image_url,
                        "wikipedia_title": wikipedia_title,
                        "summary": summary
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Saved {name} ({wikidata_id})"))

            except Exception as e:
                self.stderr.write(f"Error processing {wikidata_id}: {e}")