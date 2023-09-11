import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из CSV файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Ingredient.objects.create(
                    name = models.CharField('Название', max_length=200)
                    measurement_unit = models.CharField('Единица измерения', max_length=200)
                )

        self.stdout.write(self.style.SUCCESS('Данные успешно импортированы'))
