from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.urls import reverse_lazy
from django.db.models import Count

from .models import Article

# class GreetingView(TemplateView):
#     template_name = 'blog_greeting.html'

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

class ArticleListView(ListView):
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