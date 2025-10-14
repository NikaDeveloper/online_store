from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (удаляет старые).'

    def handle(self, *args, **options):
        # 1. Очистка базы данных
        self.stdout.write('Удаление всех данных из базы...')
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write('Данные удалены.')

        # 2. Загрузка фикстур
        self.stdout.write('Загрузка тестовых данных из фикстуры...')
        try:
            # Вызываем стандартную команду Django для загрузки фикстур
            call_command('loaddata', 'initial_data.json')
            self.stdout.write(self.style.SUCCESS('База успешно заполнена тестовыми данными!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке фикстур: {e}'))
