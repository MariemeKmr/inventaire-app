from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('sales/', include('inventaire.urls_sales', namespace='sales')),
    path("admin/", admin.site.urls),
    path("accounts/", include("inventaire.urls_accounts")),
    path("", include("inventaire.urls")),
    path("products/", include("inventaire.urls_products", namespace="products")),
    path("categories/", include("inventaire.urls_categories", namespace="categories")),

]

