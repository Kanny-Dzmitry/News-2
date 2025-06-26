import logging
from django.core.management.base import BaseCommand
from news.scheduler import start

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Запускает планировщик заданий для еженедельной рассылки новостей'

    def handle(self, *args, **options):
        self.stdout.write('Запуск планировщика заданий...')
        start() 