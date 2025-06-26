from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import News, Category, Subscription
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
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Категории'
    )
    
    class Meta:
        model = News
        fields = ['title', 'content', 'author', 'categories']

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

class CategoryList(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем информацию о подписках текущего пользователя
        if self.request.user.is_authenticated:
            subscribed_categories = Category.objects.filter(
                subscriptions__user=self.request.user
            ).values_list('id', flat=True)
            context['subscribed_categories'] = subscribed_categories
        return context

class CategoryDetail(DetailView):
    model = Category
    template_name = 'news/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        # Добавляем список новостей и статей в этой категории
        context['posts'] = News.objects.filter(categories=category).order_by('-pub_date')
        
        # Проверяем, подписан ли пользователь на эту категорию
        if self.request.user.is_authenticated:
            context['is_subscribed'] = Subscription.objects.filter(
                user=self.request.user,
                category=category
            ).exists()
        
        return context

@login_required
def subscribe_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    
    # Проверяем, не подписан ли уже пользователь
    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        category=category
    )
    
    if created:
        messages.success(request, f'Вы успешно подписались на категорию "{category.name}"')
    else:
        messages.info(request, f'Вы уже подписаны на категорию "{category.name}"')
    
    return HttpResponseRedirect(reverse('news:category_detail', args=[pk]))

@login_required
def unsubscribe_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    
    # Удаляем подписку, если она существует
    deleted, _ = Subscription.objects.filter(
        user=request.user,
        category=category
    ).delete()
    
    if deleted:
        messages.success(request, f'Вы отписались от категории "{category.name}"')
    else:
        messages.info(request, f'Вы не были подписаны на категорию "{category.name}"')
    
    return HttpResponseRedirect(reverse('news:category_detail', args=[pk]))
