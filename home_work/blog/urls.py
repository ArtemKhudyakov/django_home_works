from django.urls import path
from .views import GreetingView

app_name = "blog"

urlpatterns = [
    path("", GreetingView.as_view(), name="greeting"),
    # path("home/", HomeView.as_view(), name="home"),
    # path("contacts/", ContactsView.as_view(), name="contacts"),
    # path("product_details/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
]
