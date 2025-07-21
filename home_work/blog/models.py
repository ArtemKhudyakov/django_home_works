from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=300,
                             unique=True,
                             verbose_name="Название статьи",
                             help_text="Введите название статьи")

    author = models.CharField(max_length=100,
                              verbose_name="Автор",
                              help_text="Введите имя автора")

    content = models.TextField(verbose_name="Содержание",
                               help_text="Введите текст статьи")

    preview = models.ImageField(upload_to="blog/photos",
                                verbose_name="Изображение",
                                blank=True,
                                null=True,
                                help_text="Загрузите изображение для статьи",
                                )

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания статьи")

    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Дата обновления статьи")

    publication_status = models.BooleanField(default=False, )

    number_of_views = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['title']

    def __str__(self):
        return f'Статья "{self.title}"'
