from django.core.management.base import BaseCommand
from news.models import Category

class Command(BaseCommand):
    help = 'Создает базовые категории новостей'

    def handle(self, *args, **kwargs):
        categories = [
            'Политика',
            'Экономика',
            'Технологии',
            'Спорт',
            'Культура',
            'Наука',
            'Общество',
            'Здоровье'
        ]
        
        created_count = 0
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                created_count += 1
                self.stdout.write(f'Создана категория: {category_name}')
            else:
                self.stdout.write(f'Категория "{category_name}" уже существует')
        
        self.stdout.write(self.style.SUCCESS(f'Создано {created_count} новых категорий')) 