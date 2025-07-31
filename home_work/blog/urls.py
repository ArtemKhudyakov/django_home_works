from django.urls import path
from .views import GreetingView, ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, \
    ArticleDeleteView

app_name = "blog"

urlpatterns = [
    path("", GreetingView.as_view(), name="greeting"),
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path("articles/<int:pk>", ArticleDetailView.as_view(), name="article_detail"),
    path("articles/create", ArticleCreateView.as_view(), name="article_create"),
    path("articles/<int:pk>/update", ArticleUpdateView.as_view(), name="article_update"),
    path("articles/<int:pk>/delete", ArticleDeleteView.as_view(), name="article_delete"),
]
