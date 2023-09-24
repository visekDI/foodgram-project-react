import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из CSV файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', type=str, help='backend/recipes/data/ingredients.csv'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Ingredient.objects.create(**row)
