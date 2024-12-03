import json
from django.core.management.base import BaseCommand
from properties.models import Location

class Command(BaseCommand):
    help = 'Generate a sitemap.json file for all country locations'

    def handle(self, *args, **kwargs):
        # Query all countries (locations with location_type='country')
        countries = Location.objects.filter(location_type='country').order_by('title')

        # Initialize the sitemap structure
        sitemap = []

        for country in countries:
            country_name = country.title
            country_slug = country.country_code.lower()

            # Get the locations under each country (e.g., states)
            locations = Location.objects.filter(parent=country).order_by('title')

            # Prepare the "locations" list with the desired format
            location_list = [
                {location.title: f"{country_slug}/{location.title.lower().replace(' ', '-')}"}
                for location in locations
            ]

            # Add the country and its locations to the sitemap
            sitemap.append({
                country_name: country_slug,
                "locations": location_list
            })

        # Save the sitemap to a JSON file
        with open('sitemap.json', 'w') as json_file:
            json.dump(sitemap, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS('Sitemap generated successfully'))
