from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
import os
from pathlib import Path
from ...models import Article


class Command(BaseCommand):

    help = "Loads data to database from fixtures"

    def handle(self, *args, **options):
        #     Удаляем существующие записи
        Article.objects.all().delete()

        # Сбрасываем последовательности ID
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE blog_article_id_seq RESTART WITH 1;")

        self.stdout.write(self.style.SUCCESS("Данные успешно удалены"))

        # Загружаем фикстуру
        self.stdout.write("Loading fixture data...")
        fixture_path = (
            Path(__file__).resolve().parent.parent.parent.parent
            / "articles_fixture.json"
        )

        if not os.path.exists(fixture_path):
            self.stderr.write(f"Error: Fixture file not found at {fixture_path}")
            return

        call_command("loaddata", fixture_path)
        self.stdout.write(self.style.SUCCESS("Successfully loaded initial data!"))
