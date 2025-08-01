from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .apps import UsersConfig
from .views import CustomLogoutView, UserRegisterView

app_name = UsersConfig.name

urlpatterns = [
    path("login", LoginView.as_view(template_name = "login.html"), name="login"),
    path("logout", CustomLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
]