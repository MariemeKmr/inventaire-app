from django.urls import path
from . import views_sales

app_name = "sales"

urlpatterns = [
    path("",            views_sales.history,     name="index"),
    path("history/",    views_sales.history,     name="history"),
    path("quick/",      views_sales.quick_sale,  name="quick"),
    path("cart/",       views_sales.cart,        name="cart"),
    path("cart/add/<int:produit_id>/",    views_sales.cart_add,    name="cart_add"),
    path("cart/update/<int:produit_id>/", views_sales.cart_update, name="cart_update"),
    path("cart/remove/<int:produit_id>/", views_sales.cart_remove, name="cart_remove"),
    path("cart/clear/",                   views_sales.cart_clear,  name="cart_clear"),
    path("checkout/",   views_sales.checkout,    name="checkout"),
    path("detail/<int:sale_id>/", views_sales.detail, name="detail"),
]
