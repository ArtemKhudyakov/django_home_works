from django.http import HttpResponse
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .forms import ProductForm, ProductModeratorForm
from .models import Product, Contact, Category

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from .services.product_services import ProductServices


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

    def get_queryset(self):
        # Ключ кеша зависит от прав пользователя
        cache_key = f"products_for_user_{self.request.user.id}_is_staff_{self.request.user.is_staff}_has_perm_{self.request.user.has_perm('catalog.can_unpublish_product')}"

        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = super().get_queryset()
            if not (
                self.request.user.is_staff
                or self.request.user.has_perm("catalog.can_unpublish_product")
            ):
                queryset = queryset.filter(publication_status="published")

            # Кешируем на 15 минут (60*15)
            cache.set(cache_key, queryset, 60 * 15)

        return queryset


# class HomeView(BaseView, ListView):
#     model = Product
#     template_name = "home.html"
#     context_object_name = "latest_products"
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if not (self.request.user.is_staff or self.request.user.has_perm('catalog.can_unpublish_product')):
#             queryset = queryset.filter(publication_status='published')
#         return queryset

# def get_queryset(self):
#     # Получаем последние 5 созданных продуктов
#     latest_products = super().get_queryset().order_by("-created_at")[:5]
#     return latest_products

class CategoryProductsView(LoginRequiredMixin, BaseView, ListView):
    template_name = "category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return ProductServices.filter_products_by_category(
            category_id=self.kwargs["category_id"],
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = ProductServices.get_category_with_cache(
            self.kwargs["category_id"]
        )
        return context

# class CategoryProductsView(LoginRequiredMixin, BaseView, ListView):
#     model = Product
#     template_name = "category_products.html"
#     context_object_name = "products"
#
#     def get_queryset(self):
#         category_id = self.kwargs["category_id"]
#         return Product.objects.filter(category_id=category_id)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["current_category"] = Category.objects.get(
#             pk=self.kwargs["category_id"]
#         )
#         return context


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


@method_decorator(cache_page(15 * 60), name="dispatch")
class ProductDetailView(LoginRequiredMixin, BaseView, DetailView):
    model = Product
    template_name = "product_details.html"


# class ProductCreateView(LoginRequiredMixin, BaseView, CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = "product_form.html"
#     success_url = reverse_lazy("catalog:home")


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        print("Форма валидна! Данные:", form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("ОШИБКИ ВАЛИДАЦИИ:")
        for field, errors in form.errors.items():
            print(f"{field}: {errors}")
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, BaseView, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_update.html"
    success_url = reverse_lazy("catalog:home")

    def get_success_url(self):
        return reverse_lazy("catalog:product_details", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        return ProductForm

    def form_valid(self, form):
        # Проверяем, пытается ли пользователь изменить статус публикации
        if "publication_status" in form.changed_data:
            if not self.request.user.has_perm("catalog.can_unpublish_product"):
                form.add_error(
                    "publication_status",
                    "У вас нет прав на изменение статуса публикации",
                )
                return self.form_invalid(form)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if not (
            request.user.is_staff
            or request.user == product.owner
            or request.user.has_perm("catalog.change_product")
        ):
            messages.error(request, "У вас нет прав для редактирования этого продукта")
            return redirect("catalog:home")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, BaseView, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
    template_name = "product_delete.html"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if not (
            request.user.is_staff
            or request.user == product.owner
            or request.user.has_perm("catalog.delete_product")
        ):
            messages.error(request, "У вас нет прав для удаления этого продукта")
            return redirect("catalog:home")
        return super().dispatch(request, *args, **kwargs)


@login_required
def toggle_publish_status(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not request.user.is_authenticated:
        messages.error(request, "Требуется авторизация")
        return redirect("users:login")

    if not (
        request.user == product.owner
        or request.user.has_perm("catalog.can_unpublish_product")
    ):
        messages.error(request, "Недостаточно прав")
        return redirect("catalog:product_details", pk=product.pk)

    # Логика изменения статуса
    if product.publication_status == "published":
        product.publication_status = "draft"
        messages.success(request, "Продукт снят с публикации")
    else:
        product.publication_status = "published"
        messages.success(request, "Продукт опубликован")

    product.save()
    return redirect("catalog:product_details", pk=product.pk)
