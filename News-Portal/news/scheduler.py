import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from .tasks import send_weekly_newsletter

logger = logging.getLogger(__name__)

# Функция, которая будет удалять старые задания
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):  # 7 дней
    """
    Удаляет записи о выполнении заданий старше max_age из базы данных
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def start():
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Добавляем задачу еженедельной рассылки
    # Запускается каждый понедельник в 8:00
    scheduler.add_job(
        send_weekly_newsletter,
        trigger=CronTrigger(day_of_week="mon", hour="8", minute="0"),
        id="weekly_newsletter",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added weekly newsletter job to scheduler.")
    
    # Добавляем задачу очистки старых заданий
    # Запускается каждый день в полночь
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added weekly job: 'delete_old_job_executions'.")
    
    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!") 