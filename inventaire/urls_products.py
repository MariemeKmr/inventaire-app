from django.urls import path
from .views_products import list_products, product_create, add_product

app_name = "products"
urlpatterns = [
    path("", list_products, name="list"),
    path("new/", product_create, name="new"),
    path("add/", add_product, name="add"),
]
