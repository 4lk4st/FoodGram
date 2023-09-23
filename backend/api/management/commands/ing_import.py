import csv
import io
import os
from typing import Any

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


os.chdir('//app//data')
DATAFOLDER = os.getcwd()


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.import_ingredients()

    def import_ingredients(self):
        with io.open(DATAFOLDER + '//ingredients.csv', encoding='utf-8') as f:
            for row in csv.reader(f, delimiter=','):
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
