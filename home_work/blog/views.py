from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from .models import Article
from .forms import ArticleForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

class GreetingView(TemplateView):
    template_name = "blog_greeting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем последние 5 опубликованных статей
        context["latest_articles"] = Article.objects.filter(
            publication_status=True
        ).order_by("-created_at")[:5]
        return context


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.all()
        user = self.request.user

        # Для обычных пользователей показываем опубликованные + свои черновики
        if not (user.is_superuser or user.has_perm('blog.can_change_any_article')):
            queryset = queryset.filter(
                models.Q(publication_status=True) |
                models.Q(owner=user, publication_status=False)
            )

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Добавляем информацию о черновиках
        for article in context['articles']:
            article.is_draft = not article.publication_status
            article.can_edit = (
                    user == article.owner or
                    user.has_perm('blog.can_change_any_article')
            )
            article.can_delete = (
                    user == article.owner or
                    user.has_perm('blog.can_delete_any_article')
            )

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Добавляем флаг is_draft для каждой статьи
        for article in context['articles']:
            article.is_draft = not article.publication_status
            article.is_my_draft = (not article.publication_status) and (article.owner == user)

        # Топ авторов (только по опубликованным)
        context["top_authors"] = (
            Article.objects.filter(publication_status=True)
            .values("author")
            .annotate(article_count=Count("id"))
            .order_by("-article_count")[:3]
        )

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = context['articles']

        for article in articles:
            # Для суперпользователя и контент-менеджеров показываем статус всех статей
            if self.request.user.is_superuser or self.request.user.has_perm('blog.can_change_any_article'):
                article.is_draft = not article.publication_status
            # Для обычных пользователей - только их черновики
            else:
                article.is_draft = not article.publication_status and article.owner == self.request.user

        # Топ авторов (только по опубликованным статьям)
        context["top_authors"] = (
            Article.objects.filter(publication_status=True)
            .values("author")
            .annotate(article_count=Count("id"))
            .order_by("-article_count")[:3]
        )
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.increment_views()
        return obj


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "article_form.html"
    success_url = reverse_lazy("blog:article_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "article_form.html"
    fields = ["title", "author", "content", "preview", "publication_status"]
    success_url = reverse_lazy("blog:article_list")

    def get_success_url(self):
        return reverse_lazy("blog:article_detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if not (request.user == article.owner or request.user.has_perm('blog.can_change_any_article')):
            raise PermissionDenied("У вас нет прав на редактирование этой статьи")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if 'publication_status' in form.changed_data:
            if not self.request.user.has_perm('blog.can_publish_article'):
                form.add_error('publication_status', 'У вас нет прав на публикацию статей')
                return self.form_invalid(form)
        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')
    template_name = 'article_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if not (request.user == article.owner or request.user.has_perm('blog.can_delete_any_article')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
