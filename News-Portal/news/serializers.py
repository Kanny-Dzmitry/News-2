from rest_framework import serializers
from .models import News, Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    
    class Meta:
        model = Category
        fields = ['id', 'name']


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели News"""
    
    # Добавляем информацию о категориях
    categories = CategorySerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'pub_date', 
            'category', 'author', 'categories'
        ] 