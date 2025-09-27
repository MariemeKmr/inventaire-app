from django.urls import path
from . import views_sales

app_name = "sales"

urlpatterns = [
    path("", views_sales.history, name="index"),            # /sales/ → historique
    path("history/", views_sales.history, name="history"),
    path("detail/<int:sale_id>/", views_sales.detail, name="detail"),
    path("cart/", views_sales.cart, name="cart"),
    path("checkout/", views_sales.checkout, name="checkout"),
    path("quick/", views_sales.quick_sale, name="quick"),
]
