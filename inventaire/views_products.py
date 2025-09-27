from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Produit, Categorie
from .forms_products import ProduitForm, ProduitFilterForm, CategorieForm

def _can_edit(request):
    # À brancher sur votre logique (ex: request.user.is_staff)
    return getattr(request.user, "is_staff", False)

# --------- Produits ---------
class ProductListView(ListView):
    model = Produit
    template_name = "products/list.html"
    paginate_by = 24

    def get_queryset(self):
        qs = Produit.objects.select_related("categorie").order_by("-date_ajout")
        form = ProduitFilterForm(self.request.GET or None)
        if form.is_valid():
            q = form.cleaned_data.get("q")
            cat = form.cleaned_data.get("categorie")
            include_archived = form.cleaned_data.get("include_archived")
            if q:
                qs = qs.filter(Q(nom__icontains=q) | Q(barcode__icontains=q))
            if cat:
                qs = qs.filter(categorie=cat)
            if not include_archived:
                qs = qs.filter()  # pas d'archivage en DB pour l'instant
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = ProduitFilterForm(self.request.GET or None)
        ctx["can_edit_products"] = _can_edit(self.request)
        ctx["stock_low_threshold"] = 3
        return ctx

class ProductDetailView(DetailView):
    model = Produit
    template_name = "products/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["can_edit_products"] = _can_edit(self.request)
        ctx["stock_low_threshold"] = 3
        return ctx

class ProductCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = "products/form.html"
    success_url = reverse_lazy("products:list")

    def dispatch(self, request, *args, **kwargs):
        if not _can_edit(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Réservé à l’admin.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Produit ajouté.")
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = "products/form.html"
    success_url = reverse_lazy("products:list")

    def dispatch(self, request, *args, **kwargs):
        if not _can_edit(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Réservé à l’admin.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Produit modifié.")
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Produit
    template_name = "products/confirm_delete.html"
    success_url = reverse_lazy("products:list")

    def dispatch(self, request, *args, **kwargs):
        if not _can_edit(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Réservé à l’admin.")
        return super().dispatch(request, *args, **kwargs)

# --------- Catégories ---------
class CategoryListView(ListView):
    model = Categorie
    template_name = "categories/index.html"
    context_object_name = "categories"

    def dispatch(self, request, *args, **kwargs):
        if not _can_edit(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Réservé à l’admin.")
        return super().dispatch(request, *args, **kwargs)

class CategoryCreateView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = "categories/form.html"
    success_url = reverse_lazy("categories:index")

    def dispatch(self, request, *args, **kwargs):
        if not _can_edit(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Réservé à l’admin.")
        return super().dispatch(request, *args, **kwargs)

class CategoryUpdateView(UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = "categories/form.html"
    success_url = reverse_lazy("categories:index")

    def dispatch(self, request, *args, **kwargs):
        if not _can_edit(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Réservé à l’admin.")
        return super().dispatch(request, *args, **kwargs)

class CategoryDeleteView(DeleteView):
    model = Categorie
    template_name = "categories/confirm_delete.html"
    success_url = reverse_lazy("categories:index")

    def dispatch(self, request, *args, **kwargs):
        if not _can_edit(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Réservé à l’admin.")
        return super().dispatch(request, *args, **kwargs)
