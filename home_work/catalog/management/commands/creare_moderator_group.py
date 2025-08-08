from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from ...models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов с разрешениями для модератора'

    def handle(self, *args, **options):
        # Создаем группу
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Получаем нужные разрешения
        permissions = Permission.objects.filter(
            codename__in=[
                'can_unpublish_product',
                'delete_product',
            ]
        )

        # Добавляем разрешения в группу
        group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" обновлена'))