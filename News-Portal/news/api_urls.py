from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import NewsViewSet, ArticleViewSet, CategoryViewSet

# Настройка маршрутов для API
router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news-api')
router.register(r'articles', ArticleViewSet, basename='article-api')
router.register(r'categories', CategoryViewSet, basename='category-api')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
] 