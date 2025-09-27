from django.urls import path
from . import views_products as v

app_name = "products"

urlpatterns = [
    path("", v.ProductListView.as_view(), name="list"),
    path("<int:pk>/", v.ProductDetailView.as_view(), name="detail"),
    path("new/", v.ProductCreateView.as_view(), name="new"),
    path("<int:pk>/edit/", v.ProductUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", v.ProductDeleteView.as_view(), name="delete"),
]
