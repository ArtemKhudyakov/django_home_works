
from django.db import models
import os

from home_work.config.settings import BASE_DIR


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]

    def __str__(self):
        return f'Категория "{self.name}"'


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to= os.path.join(BASE_DIR, "catalog/photos"),
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id"]

    def __str__(self):
        return f'Продукт "{self.name}"'
