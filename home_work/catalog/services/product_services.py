from django.core.cache import cache
from ..models import Product, Category


class ProductServices:
    @staticmethod
    def filter_products_by_category(category_id, user):
        """
        Возвращает продукты категории с учётом прав пользователя
        """
        cache_key = f"category_{category_id}_products_user_{user.id}_staff_{user.is_staff}_perm_{user.has_perm('catalog.can_unpublish_product')}"
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Product.objects.filter(category_id=category_id).select_related('category')

            if not (user.is_staff or user.has_perm('catalog.can_unpublish_product')):
                queryset = queryset.filter(publication_status='published')

            cache.set(cache_key, queryset, 60 * 15)  # 15 минут кеш

        return queryset

    @staticmethod
    def get_category_with_cache(category_id):
        """
        Возвращает категорию с кешированием
        """
        cache_key = f"category_{category_id}_full"
        category = cache.get(cache_key)

        if category is None:
            category = Category.objects.get(pk=category_id)
            cache.set(cache_key, category, 60 * 60 * 24)  # 1 день кеш

        return category