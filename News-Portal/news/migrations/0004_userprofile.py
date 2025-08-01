# Generated by Django 5.2.3 on 2025-07-04 17:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_category_news_categories_subscription_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(choices=[('Europe/Moscow', 'Москва'), ('Europe/London', 'Лондон'), ('America/New_York', 'Нью-Йорк'), ('America/Chicago', 'Чикаго'), ('America/Denver', 'Денвер'), ('America/Los_Angeles', 'Лос-Анджелес'), ('Asia/Tokyo', 'Токио'), ('Asia/Shanghai', 'Шанхай'), ('Asia/Dubai', 'Дубай'), ('Australia/Sydney', 'Сидней'), ('UTC', 'UTC')], default='UTC', max_length=50, verbose_name='Часовой пояс')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
    ]
