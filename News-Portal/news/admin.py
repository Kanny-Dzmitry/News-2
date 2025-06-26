from django.contrib import admin
from .models import News, Category, Subscription

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'pub_date', 'author')
    list_filter = ('category', 'pub_date', 'author')
    search_fields = ('title', 'content')
    filter_horizontal = ('categories',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'date_subscribed')
    list_filter = ('category', 'date_subscribed')
    search_fields = ('user__username', 'category__name')
    date_hierarchy = 'date_subscribed'
