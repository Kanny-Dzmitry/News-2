from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.core.cache import cache
from .models import News, Category, Subscription
from .tasks import send_notification_about_new_post
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        try:
            common_group = Group.objects.get(name='common')
            instance.groups.add(common_group)
        except Group.DoesNotExist:
            # If the group doesn't exist, we'll just skip
            pass
            
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Отправляет приветственное письмо при регистрации пользователя"""
    if created:
        subject = 'Добро пожаловать на News Portal!'
        text_content = (
            f'Здравствуйте, {instance.username}!\n\n'
            f'Добро пожаловать на наш новостной портал. '
            f'Теперь вы можете читать новости и статьи, а также подписываться на интересующие вас категории.'
        )
        html_content = render_to_string(
            'news/email/welcome_email.html',
            {
                'username': instance.username,
            }
        )
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else None,
            to=[instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        
        try:
            msg.send()
            logger.info(f'Welcome email sent to {instance.email}')
        except Exception as e:
            logger.error(f'Failed to send welcome email: {e}')

@receiver(m2m_changed, sender=News.categories.through)
def notify_about_new_post(sender, instance, action, pk_set, **kwargs):
    """Отправляет уведомление подписчикам при создании новой статьи"""
    if action == 'post_add' and pk_set:
        # Запускаем асинхронную задачу для отправки уведомлений
        send_notification_about_new_post.delay(
            post_id=instance.id,
            category_ids=list(pk_set)
        )
        logger.info(f'Notification task queued for post {instance.id}')

@receiver(m2m_changed, sender=News.categories.through)
def news_categories_changed(sender, instance, action, **kwargs):
    """Очищаем кэш при изменении категорий новости/статьи"""
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Очищаем кэш новости/статьи
        cache.delete(f'news_obj_{instance.pk}')
        
        if instance.category == News.NEWS:
            cache.delete('news_list_page')
        else:
            cache.delete('article_list_page')
        
        # Очищаем кэш категорий
        for category_id in kwargs.get('pk_set', []):
            cache.delete(f'category-{category_id}')

@receiver(post_save, sender=Subscription)
def subscription_changed(sender, instance, created, **kwargs):
    """Очищаем кэш при изменении подписок"""
    # Очищаем кэш категории
    cache.delete(f'category-{instance.category.id}')

@receiver(post_delete, sender=Subscription)
def subscription_deleted(sender, instance, **kwargs):
    """Очищаем кэш при удалении подписки"""
    # Очищаем кэш категории
    cache.delete(f'category-{instance.category.id}') 