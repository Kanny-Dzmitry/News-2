import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)

# Этот файл больше не используется для планирования задач, так как мы перешли на Celery
# Оставлен для обратной совместимости с существующим кодом
# Все задачи теперь настраиваются в NewsPortal/celery.py

def start():
    logger.info("Scheduler is deprecated. Using Celery for task scheduling.") 