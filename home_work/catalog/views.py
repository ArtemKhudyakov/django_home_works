from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.urls import reverse_lazy

from .models import Product, Contact


# def greeting(request):
#     return render(request, 'greeting.html')

class GreetingView(TemplateView):
    template_name = 'greeting.html'


# def home(request):
#     # Получаем последние 5 созданных продуктов
#     latest_products = Product.objects.order_by("-created_at")[:5]
#
#     context = {'latest_products': latest_products}
#     # Выводим в консоль
#     print("Последние 5 добавленных продуктов:")
#     for product in latest_products:
#         print(f"{product.name} - {product.created_at}")
#
#     return render(request, "home.html", context)


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        # Получаем последние 5 созданных продуктов
        latest_products = super().get_queryset().order_by("-created_at")[:5]
        return latest_products

# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         return HttpResponse(
#             f"""
#             Спасибо, {name}. Ваше сообщение успешно отправлено!
#     Мы свяжемся с Вами по номеру телефона {phone}"""
#         )
#
#     # Получаем контактные данные из базы
#     contact_info = Contact.objects.first()
#     return render(request, "contacts.html", {"contact_info": contact_info})

class ContactsView(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = Contact.objects.first()
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

# def product_details(request, pk):
#     product = Product.objects.get(pk=pk)
#     context = {"product": product}
#     return render(request, "product_details.html", context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'





