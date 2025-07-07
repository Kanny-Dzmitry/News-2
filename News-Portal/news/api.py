from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer


class NewsViewSet(viewsets.ModelViewSet):
    """API представление для модели News (новости)"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NewsSerializer
    
    def get_queryset(self):
        """Возвращает только объекты с категорией NEWS"""
        return News.objects.filter(category=News.NEWS)
    
    def perform_create(self, serializer):
        """Устанавливает автора и категорию при создании"""
        serializer.save(
            author=self.request.user,
            category=News.NEWS
        )


class ArticleViewSet(viewsets.ModelViewSet):
    """API представление для модели News (статьи)"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NewsSerializer
    
    def get_queryset(self):
        """Возвращает только объекты с категорией ARTICLE"""
        return News.objects.filter(category=News.ARTICLE)
    
    def perform_create(self, serializer):
        """Устанавливает автора и категорию при создании"""
        serializer.save(
            author=self.request.user,
            category=News.ARTICLE
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """API представление для модели Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 