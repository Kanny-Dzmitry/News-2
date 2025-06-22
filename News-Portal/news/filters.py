import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import News

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Заголовок содержит'
    )
    
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )
    
    pub_date__gt = django_filters.DateFilter(
        field_name='pub_date',
        lookup_expr='gt',
        label='Опубликовано после',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = News
        fields = ['title', 'author', 'pub_date__gt'] 