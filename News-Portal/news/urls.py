from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsSearch, 
    NewsCreate, NewsEdit, NewsDelete,
    ArticleList, ArticleDetail,
    ArticleCreate, ArticleEdit, ArticleDelete,
    CategoryList, CategoryDetail,
    subscribe_category, unsubscribe_category,
    become_author, timezone_settings, user_profile
)

app_name = 'news'

urlpatterns = [
    # Новости
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    
    # Статьи
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    
    # Категории
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('categories/<int:pk>/subscribe/', subscribe_category, name='subscribe_category'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe_category, name='unsubscribe_category'),
    
    # Профиль
    path('become-author/', become_author, name='become_author'),
    path('timezone-settings/', timezone_settings, name='timezone_settings'),
    path('profile/', user_profile, name='user_profile'),
] 