from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ...models import Article


class Command(BaseCommand):
    help = 'Creates Content Managers group with permissions'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(name='Контент-менеджеры')

        if created:
            # Получаем нужные права
            content_type = ContentType.objects.get_for_model(Article)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=[
                    'can_publish_article',
                    'can_change_any_article',
                    'can_delete_any_article',
                    'add_article',
                    'change_article',
                    'delete_article',
                    'view_article'
                ]
            )

            # Добавляем права в группу
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджеры" создана с правами'))
        else:
            self.stdout.write(self.style.WARNING('Группа уже существует'))