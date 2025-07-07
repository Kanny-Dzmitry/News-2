from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(
        User,
        through='Subscription',
        related_name='categories',
        verbose_name='Подписчики'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Категория'
    )
    date_subscribed = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'category')

    def __str__(self):
        return f'{self.user.username} - {self.category.name}'

class News(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    category = models.CharField(
        max_length=2, 
        choices=CATEGORY_CHOICES, 
        default=NEWS, 
        verbose_name='Категория'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='news',
        verbose_name='Автор',
        null=True,
        blank=True
    )
    categories = models.ManyToManyField(
        Category,
        related_name='news',
        verbose_name='Категории'
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        if self.category == self.NEWS:
            return reverse('news:news_detail', args=[str(self.id)])
        else:
            return reverse('news:article_detail', args=[str(self.id)])

    def preview(self):
        """Возвращает первые 124 символа содержания статьи"""
        return f"{self.content[:124]}..." if len(self.content) > 124 else self.content
    
    def save(self, *args, **kwargs):
        """Переопределяем метод save для автоматической очистки кэша"""
        # Очищаем кэш при сохранении/изменении новости или статьи
        is_new = self.pk is None
        
        # Сохраняем объект
        super().save(*args, **kwargs)
        
        # Очищаем кэш
        if self.category == self.NEWS:
            cache.delete(f'news-{self.pk}')
            cache.delete('news_list_page')
        else:
            cache.delete(f'article-{self.pk}')
            cache.delete('article_list_page')
        
        # Очищаем кэш категорий, к которым относится новость
        for category in self.categories.all():
            cache.delete(f'category-{category.pk}')
    
    def delete(self, *args, **kwargs):
        """Переопределяем метод delete для автоматической очистки кэша"""
        # Сохраняем категории перед удалением
        category_ids = list(self.categories.values_list('id', flat=True))
        
        # Определяем тип (новость или статья)
        is_news = self.category == self.NEWS
        
        # Удаляем объект
        result = super().delete(*args, **kwargs)
        
        # Очищаем кэш
        if is_news:
            cache.delete(f'news-{self.pk}')
            cache.delete('news_list_page')
        else:
            cache.delete(f'article-{self.pk}')
            cache.delete('article_list_page')
        
        # Очищаем кэш категорий
        for category_id in category_ids:
            cache.delete(f'category-{category_id}')
        
        return result
    
    @classmethod
    def get_cached_by_id(cls, pk):
        """Получает объект News из кэша или из базы данных"""
        obj = cache.get(f'news_obj_{pk}')
        if not obj:
            obj = cls.objects.get(pk=pk)
            cache.set(f'news_obj_{pk}', obj, timeout=300)  # Кэшируем на 5 минут
        return obj


class UserProfile(models.Model):
    """Профиль пользователя с дополнительными настройками"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    timezone = models.CharField(
        max_length=50,
        choices=settings.TIMEZONE_FIELD_CHOICES if hasattr(settings, 'TIMEZONE_FIELD_CHOICES') else [('UTC', 'UTC')],
        default='UTC',
        verbose_name='Часовой пояс'
    )
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаем профиль пользователя при регистрации"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль пользователя при обновлении"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)
