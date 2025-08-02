from django.http import HttpResponse
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .forms import ProductForm
from .models import Product, Contact, Category


class BaseView(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_categories"] = Category.objects.all()
        return context


class GreetingView(BaseView, TemplateView):
    template_name = "greeting.html"


class HomeView(BaseView, ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "latest_products"

    # def get_queryset(self):
    #     # Получаем последние 5 созданных продуктов
    #     latest_products = super().get_queryset().order_by("-created_at")[:5]
    #     return latest_products


class CategoryProductsView(LoginRequiredMixin, BaseView, ListView):
    model = Product
    template_name = "category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = Category.objects.get(
            pk=self.kwargs["category_id"]
        )
        return context


class ContactsView(TemplateView, BaseView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_info"] = Contact.objects.first()
        return context

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"""
            Спасибо, {name}. Ваше сообщение успешно отправлено!
            Мы свяжемся с Вами по номеру телефона {phone}"""
        )


class ProductDetailView(LoginRequiredMixin, BaseView, DetailView):
    model = Product
    template_name = "product_details.html"


class ProductCreateView(LoginRequiredMixin, BaseView, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(LoginRequiredMixin, BaseView, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_update.html"
    success_url = reverse_lazy("catalog:home")

    def get_success_url(self):
        return reverse_lazy("catalog:product_details", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, BaseView, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
    template_name = "product_delete.html"
