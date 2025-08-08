from django.db import models
from django.conf import settings


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
    # Варианты статусов для поля choices
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (DRAFT, 'Черновик'),
        (PUBLISHED, 'Опубликовано'),
        (ARCHIVED, 'В архиве'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="catalog/photos",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения"
    )

    # Новое поле для статуса публикации
    publication_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
        verbose_name="Статус публикации",
        help_text="Выберите статус публикации продукта"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        related_name="products"
    )


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id"]
        permissions = [('can_unpublish_product', 'Can unpublish product')]

    def __str__(self):
        return f'Продукт "{self.name}"'


class Contact(models.Model):
    country = models.CharField(max_length=100, verbose_name="Страна")
    inn = models.CharField(max_length=20, verbose_name="ИНН")
    address = models.TextField(verbose_name="Адрес")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"Контактные данные ({self.country})"
