from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "password", "country", "phone", "avatar", "is_staff", "is_superuser", "is_active", "is_verified")
    search_fields = ("username", "email", "phone")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_verified", "groups")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
