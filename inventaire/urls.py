from django.urls import path, include
from .views_dashboard import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("products/", include("inventaire.urls_products", namespace="products")),
    path("sales/", include("inventaire.urls_sales", namespace="sales")),
    path("debts/", include("inventaire.urls_debts", namespace="debts")),
    path("stats/", include("inventaire.urls_stats", namespace="stats")),
    path("history/", include("inventaire.urls_history", namespace="history")),
    path("replenish/", include("inventaire.urls_replenish", namespace="replenish")),
]
