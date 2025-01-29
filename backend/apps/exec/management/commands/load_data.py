# docker-compose -f ./.docker/docker-compose.dev.yml exec backend bash -c "cd backend && python manage.py shell -c 'exec(open(\"apps/utils/load_data.py\").read())'"

import os
import csv
from apps.categories.models import Category
from apps.collections.models import Collection
from apps.registry.models import University, Major
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load data from CSV files into the database"

    def handle(self, *args, **options):
        self.load_universities()
        self.load_majors()
        self.load_categories()
        self.load_collections()

    def load_universities(self):
        with open(
            os.path.abspath("apps/exec/management/commands/data/universities_Russia.csv")
        ) as f:
            reader = csv.reader(f)
            for row in reader:
                if University.objects.filter(name=row[0]).exists():
                    continue
                University.objects.get_or_create(
                    name=row[0],
                    city=row[1],
                    country="Россия",
                )
        self.stdout.write(self.style.SUCCESS("Universities loaded successfully."))

    def load_majors(self):
        with open(
            os.path.abspath("apps/exec/management/commands/data/majors_Russia.csv")
        ) as f:
            reader = csv.reader(f)
            for row in reader:
                if Major.objects.filter(name=row[1]).exists():
                    continue
                Major.objects.get_or_create(
                    name=row[0],
                    code=row[1],
                )
        self.stdout.write(self.style.SUCCESS("Majors loaded successfully."))

    def load_categories(self):
        with open(os.path.abspath("apps/exec/management/commands/data/categories.csv")) as f:
            reader = csv.reader(f)
            for row in reader:
                if Category.objects.filter(name=row[0]).exists():
                    continue
                Category.objects.get_or_create(
                    name=row[0],
                    description=row[1],
                )
        self.stdout.write(self.style.SUCCESS("Categories loaded successfully."))

    def load_collections(self):
        with open(
            os.path.abspath("apps/exec/management/commands/data/collections.csv")
        ) as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if Collection.objects.filter(name=row[0]).exists():
                    continue
                Collection.objects.get_or_create(
                    name=row[0],
                    description=row[1],
                    emoji=row[2],
                )
        self.stdout.write(self.style.SUCCESS("Collections loaded successfully."))
