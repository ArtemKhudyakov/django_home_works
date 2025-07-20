from django.urls import path
from .views import HomeView, ContactsView, GreetingView, ProductDetailView

app_name = "catalog"

urlpatterns = [
    path("", GreetingView.as_view(), name="greeting"),
    path("home/", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product_details/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
]
