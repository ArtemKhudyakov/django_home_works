from django.urls import path
from .views import home, contacts, base
app_name = "catalog"

urlpatterns = [
    path("", base, name="base"),
    path("home/", home, name="home"),
    path("contacts/", contacts, name="contacts"),
]
