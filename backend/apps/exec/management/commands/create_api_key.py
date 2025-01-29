from rest_framework_api_key.models import APIKey
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a new API key"

    def handle(self, *args, **kwargs):
        api_key, key = APIKey.objects.create_key(name="TYF_API_KEY")
        self.stdout.write(self.style.SUCCESS(f"API Key created: {key}"))
