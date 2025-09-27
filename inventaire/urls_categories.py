from django.urls import path
from . import views_products as v

app_name = "categories"

urlpatterns = [
    path("", v.CategoryListView.as_view(), name="index"),
    path("new/", v.CategoryCreateView.as_view(), name="new"),
    path("<int:pk>/edit/", v.CategoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", v.CategoryDeleteView.as_view(), name="delete"),
]
