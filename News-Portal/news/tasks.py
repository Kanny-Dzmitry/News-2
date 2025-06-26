import logging
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from .models import News, Category, Subscription

logger = logging.getLogger(__name__)

def send_weekly_newsletter():
    """
    Отправляет еженедельную рассылку новостей подписчикам
    """
    # Определяем период - последние 7 дней
    week_ago = timezone.now() - timedelta(days=7)
    
    # Получаем все категории
    categories = Category.objects.all()
    
    # Для каждой категории находим новые статьи и отправляем подписчикам
    for category in categories:
        # Получаем новые статьи в данной категории за последнюю неделю
        new_posts = News.objects.filter(
            categories=category,
            pub_date__gte=week_ago
        ).order_by('-pub_date')
        
        # Если нет новых статей, пропускаем категорию
        if not new_posts:
            continue
        
        # Получаем всех подписчиков категории
        subscribers = User.objects.filter(
            subscriptions__category=category
        ).distinct()
        
        # Для каждого подписчика формируем и отправляем письмо
        for subscriber in subscribers:
            # Формируем список статей для шаблона
            posts_for_user = []
            for post in new_posts:
                posts_for_user.append({
                    'title': post.title,
                    'preview': post.preview(),
                    'url': f'http://127.0.0.1:8000{post.get_absolute_url()}',
                    'pub_date': post.pub_date,
                    'type': post.get_category_display(),
                })
            
            # Формируем и отправляем письмо
            subject = f'Еженедельная рассылка новостей: {category.name}'
            
            text_content = (
                f'Здравствуйте, {subscriber.username}!\n\n'
                f'Новые публикации в категории "{category.name}" за последнюю неделю:\n\n'
            )
            
            for post in posts_for_user:
                text_content += f'- {post["title"]} ({post["pub_date"].strftime("%d.%m.%Y")})\n'
                text_content += f'  {post["preview"]}\n'
                text_content += f'  Ссылка: {post["url"]}\n\n'
            
            html_content = render_to_string(
                'news/email/weekly_newsletter.html',
                {
                    'username': subscriber.username,
                    'category': category.name,
                    'posts': posts_for_user,
                    'week_start': week_ago.strftime("%d.%m.%Y"),
                    'week_end': timezone.now().strftime("%d.%m.%Y"),
                }
            )
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else None,
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            
            try:
                msg.send()
                logger.info(f'Weekly newsletter for category {category.name} sent to {subscriber.email}')
            except Exception as e:
                logger.error(f'Failed to send weekly newsletter: {e}') 