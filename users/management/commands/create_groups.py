from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from blog.models import BlogEntry as Blog
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Создает группы Модератор продуктов и Контент-менеджер с соответствующими правами.'

    def handle(self, *args, **kwargs):
        moderator_permissions = [
            'can_unpublish_product',
            'delete_product',
        ]

        try:
            moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
            if created:
                self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана.'))
            else:
                self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует.'))

            product_content_type = ContentType.objects.get_for_model(Product)

            for codename in moderator_permissions:
                try:
                    permission = Permission.objects.get(
                        codename=codename,
                        content_type=product_content_type
                    )
                    moderator_group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'  - Право "{codename}" назначено.'))
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'  - Право "{codename}" не найдено! Убедитесь, что миграции выполнены.'))


            blog_content_type = ContentType.objects.get_for_model(Blog)

            content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
            if created:
                self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" создана.'))
            else:
                self.stdout.write(self.style.WARNING('Группа "Контент-менеджер" уже существует.'))

            for codename_prefix in ['add', 'change', 'delete', 'view']:
                codename = f'{codename_prefix}_blogentry'
                try:
                    permission = Permission.objects.get(
                        codename=codename,
                        content_type=blog_content_type
                    )
                    content_manager_group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'  - Право "{codename}" назначено.'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'  - Право "{codename}" не найдено!'))

        except IntegrityError:
            self.stdout.write(self.style.ERROR('Ошибка создания группы: Проверьте базу данных.'))

        except ContentType.DoesNotExist:
            self.stdout.write(self.style.ERROR('Ошибка: Модели Product или Blog не найдены. Проверьте INSTALLED_APPS.'))

        self.stdout.write(self.style.SUCCESS('Настройка групп завершена.'))
