from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

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
