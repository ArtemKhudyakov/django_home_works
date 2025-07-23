from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.urls import reverse_lazy

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
