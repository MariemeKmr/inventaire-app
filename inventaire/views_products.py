# views_products.py (exemples avec CBV)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from django.urls import reverse_lazy

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 25
    ordering = ["name"]

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product

class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = "app.add_product"
    model = Product
    fields = ["sku","name","category","uom","reorder_level","is_active"]

class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "app.change_product"
    model = Product
    fields = ["sku","name","category","uom","reorder_level","is_active"]

class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "app.delete_product"
    model = Product
    success_url = reverse_lazy("product_list")
