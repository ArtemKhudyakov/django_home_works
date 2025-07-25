from django.urls import path
from .views import GreetingView, ArticleListView

app_name = "blog"

urlpatterns = [
    path("", GreetingView.as_view(), name="greeting"),
    path("articles/", ArticleListView.as_view(), name="article_list"),
    # path("home/", HomeView.as_view(), name="home"),
    # path("contacts/", ContactsView.as_view(), name="contacts"),
    # path("product_details/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
]
