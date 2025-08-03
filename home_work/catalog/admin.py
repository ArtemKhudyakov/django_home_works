from django.contrib import admin
from .models import Product, Category, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "publication_status",
    )
    list_filter = ("category", "publication_status",)
    search_fields = (
        "name",
        "description",
        "publication_status",
    )
    list_editable = ("name", "price", "publication_status")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("country", "inn", "address")
    search_fields = ("country", "inn")
