from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from .models import Article


class GreetingView(TemplateView):
    template_name = 'blog_greeting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем последние 5 опубликованных статей
        context['latest_articles'] = Article.objects.filter(
            publication_status=True
        ).order_by('-created_at')[:5]
        return context

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):

        return Article.objects.filter(
            publication_status=True
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем топ-3 авторов по количеству статей
        context['top_authors'] = Article.objects.values(
            'author'
        ).annotate(
            article_count=Count('id')
        ).order_by('-article_count')[:3]
        return context

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.increment_views()
        return obj

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_form.html'
    fields = ['title', 'author', 'content', 'preview', 'publication_status']
    success_url = reverse_lazy('blog:article_list')


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'article_form.html'
    fields = ['title', 'author', 'content', 'preview', 'publication_status']
    success_url = reverse_lazy('blog:article_list')

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')
    template_name = 'article_confirm_delete.html'
