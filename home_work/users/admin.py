from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("id", "username", "email", "country", "phone", "avatar", "is_staff", "is_superuser")
    search_fields = ("username", "email", "phone")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_verified", "groups")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    list_editable = ("username", "email", "country", "phone", "avatar", "is_staff", "is_superuser",)
    exclude = ('password',)


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import Group
# from .models import User
#
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):  # Наследуемся от BaseUserAdmin, а не admin.ModelAdmin
#     list_display = ('email', 'username', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'password')}),
#         ('Personal info', {'fields': ('country', 'phone', 'avatar')}),
#         ('Permissions', {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email', 'username')
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions',)