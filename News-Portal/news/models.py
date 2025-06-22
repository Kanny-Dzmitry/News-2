from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

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
