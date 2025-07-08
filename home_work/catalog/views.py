from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact


def home(request):
    # Получаем последние 5 созданных продуктов
    latest_products = Product.objects.order_by("-created_at")[:5]

    # Выводим в консоль
    print("Последние 5 добавленных продуктов:")
    for product in latest_products:
        print(f"{product.name} - {product.created_at}")

    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"""
            Спасибо, {name}. Ваше сообщение успешно отправлено!
    Мы свяжемся с Вами по номеру телефона {phone}"""
        )

    # Получаем контактные данные из базы
    contact_info = Contact.objects.first()
    return render(request, "contacts.html", {"contact_info": contact_info})


# from django.shortcuts import render
# from django.http import HttpResponse
#
#
# # Create your views here.
#
#
# def home(request):
#     return render(request, "home.html")
#
#
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
#     return render(request, "contacts.html")
