from django.urls import path
from .views import (
    HomeView,
    ContactsView,
    GreetingView,
    ProductDetailView,
    ProductCreateView,
    CategoryProductsView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = "catalog"

urlpatterns = [
    path("", GreetingView.as_view(), name="greeting"),
    path("home/", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path(
        "product_details/<int:pk>/", ProductDetailView.as_view(), name="product_details"
    ),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "category/<int:category_id>/",
        CategoryProductsView.as_view(),
        name="category_products",
    ),
    path(
        "product_update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product_delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"
    ),
]
