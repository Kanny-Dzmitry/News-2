from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsSearch, 
    NewsCreate, NewsEdit, NewsDelete,
    ArticleList, ArticleDetail,
    ArticleCreate, ArticleEdit, ArticleDelete,
    become_author
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
    
    # Профиль
    path('become-author/', become_author, name='become_author'),
] 