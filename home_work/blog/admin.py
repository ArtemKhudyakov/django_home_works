from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "content",
        "preview",
        "created_at",
        "updated_at",
        "publication_status",
        "number_of_views",
    )

    list_filter = ("publication_status", "number_of_views", "author")

    search_fields = ("title", "content")
