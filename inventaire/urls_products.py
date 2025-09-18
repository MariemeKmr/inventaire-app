from django.urls import path
from .views_products import list_products, new_product

app_name = "products"
urlpatterns = [
    path("", list_products, name="list"),
    path("new/", new_product, name="new"),
]
