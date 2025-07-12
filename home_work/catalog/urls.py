from django.urls import path
from .views import home, contacts, greeting, product_details

app_name = "catalog"

urlpatterns = [
    path("", greeting, name="greeting"),
    path("home/", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product_details/<int:pk>/", product_details, name="product_details"),
]
