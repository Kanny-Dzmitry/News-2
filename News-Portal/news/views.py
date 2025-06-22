from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import View
from .models import News
from .filters import NewsFilter
from django import forms

# Create your views here.

class NewsList(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10  # Пагинация по 10 новостей на странице
    
    def get_queryset(self):
        queryset = News.objects.filter(category=News.NEWS)
        return queryset

class NewsDetail(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

class ArticleList(ListView):
    model = News
    template_name = 'news/article_list.html'
    context_object_name = 'article_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = News.objects.filter(category=News.ARTICLE)
        return queryset

class ArticleDetail(DetailView):
    model = News
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

class NewsSearch(ListView):
    model = News
    template_name = 'news/news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = News.objects.all()
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'author']

class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    permission_required = ('news.add_news',)
    
    def form_valid(self, form):
        news = form.save(commit=False)
        news.category = News.NEWS
        return super().form_valid(form)

class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    permission_required = ('news.change_news',)

class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:news_list')
    permission_required = ('news.delete_news',)
    
    def get_queryset(self):
        return News.objects.filter(category=News.NEWS)

class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/article_edit.html'
    permission_required = ('news.add_news',)
    
    def form_valid(self, form):
        article = form.save(commit=False)
        article.category = News.ARTICLE
        return super().form_valid(form)

class ArticleEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/article_edit.html'
    permission_required = ('news.change_news',)
    
    def get_queryset(self):
        return News.objects.filter(category=News.ARTICLE)

class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('news:article_list')
    permission_required = ('news.delete_news',)
    
    def get_queryset(self):
        return News.objects.filter(category=News.ARTICLE)

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        user.groups.add(authors_group)
    return redirect('news:news_list')
