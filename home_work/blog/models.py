from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(
        max_length=300,
        unique=True,
        verbose_name="Название статьи",
        help_text="Введите название статьи",
    )

    author = models.CharField(
        max_length=100, verbose_name="Автор", help_text="Введите имя автора"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Владелец",
        related_name="articles",
    )

    content = models.TextField(
        verbose_name="Содержание", help_text="Введите текст статьи"
    )

    preview = models.ImageField(
        upload_to="blog/photos",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение для статьи",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания статьи"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления статьи"
    )

    publication_status = models.BooleanField(
        default=False,
    )

    number_of_views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    def increment_views(self):
        self.number_of_views += 1
        self.save(update_fields=["number_of_views"])

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["title"]
        permissions = [
            ("can_publish_article", "Может публиковать статьи"),
            ("can_change_any_article", "Может изменять любые статьи"),
            ("can_delete_any_article", "Может удалять любые статьи"),
        ]

    def __str__(self):
        return f'Статья "{self.title}"'
