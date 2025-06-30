from django.urls import path
from .views import home, contacts

app_name = "catalog"

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contacts, name='contacts'),
]