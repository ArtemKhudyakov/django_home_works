from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:greeting')


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('blog:greeting')  # Или ваш стартовый URL

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Регистрация прошла успешно!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)