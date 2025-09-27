from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms_products import ProductForm
from .models import Produit, Categorie
from django.db.models import Q
from django.core.paginator import Paginator
# views_products.py

@login_required(login_url="/admin/login/")
def list_products(request):
    q = (request.GET.get("q") or "").strip()
    cat = (request.GET.get("cat") or "").strip()     # valeur = nom de la catégorie (PK texte)
    sort = (request.GET.get("sort") or "-date_ajout").strip()
    page_number = request.GET.get("page") or 1
    per_page = int(request.GET.get("per_page") or 12)
    low_stock_threshold = 3

    # Base queryset + jointure catégorie
    qs = Produit.objects.select_related("categorie")

    # Recherche texte (nom produit, code-barres, nom catégorie)
    if q:
        qs = qs.filter(
            Q(nom__icontains=q) |
            Q(barcode__icontains=q) |
            Q(categorie__nom__icontains=q)
        )

    # Filtre catégorie (PK = nom)
    if cat:
        qs = qs.filter(categorie__nom=cat)

    # Tri simple (sécurise un minimum les champs autorisés)
    allowed_sorts = {"nom", "-nom", "date_ajout", "-date_ajout", "prix_vente", "-prix_vente", "quantite", "-quantite"}
    if sort not in allowed_sorts:
        sort = "-date_ajout"
    qs = qs.order_by(sort, "-pk")

    # Pagination
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Transforme en dicts compatibles avec ton template démo
    products = []
    for p in page_obj.object_list:
        # image: priorise l'upload si présent, sinon l'URL stockée
        img = None
        if getattr(p, "image_file", None):
            try:
                if p.image_file:
                    img = p.image_file.url
            except Exception:
                img = None
        if not img:
            img = p.image_url

        products.append({
            "id": p.pk,
            "nom": p.nom,
            "prix_vente": p.prix_vente,
            "quantite": p.quantite,
            "image_url": img,
            "categorie": {
                # PK texte = nom ; on expose "id" pour rester compatible
                "id": p.categorie_id,  # == nom si non nul
                "nom": p.categorie.nom if p.categorie else None,
            },
        })

    # On remplace l'object_list par nos dicts (le reste du Page est intact: has_next, etc.)
    page_obj.object_list = products

    # Liste des catégories pour les filtres (clé "id" = nom)
    categories = [{"id": c.nom, "nom": c.nom} for c in Categorie.objects.order_by("nom")]

    ctx = {
        "categories": categories,
        "page_obj": page_obj,
        "low_stock_threshold": low_stock_threshold,
        "q": q,
        "selected_cat": cat,
        "sort": sort,
        "per_page": per_page,
    }
    return render(request, "products/list.html", ctx)

@login_required(login_url="/admin/login/")
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)  # Crée une instance mais ne sauvegarde pas encore
            produit.save()  # Sauvegarde dans la base de données
            messages.success(request, "Produit enregistré avec succès.")
            return redirect("products:list")
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = ProductForm()

    return render(request, "products/new.html", {"form": form})

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit enregistré avec succès.")
            return redirect("products:list")
        else:
            messages.error(request, "Corrige les erreurs du formulaire.")
    else:
        form = ProductForm()
    return render(request, "products/add.html", {"form": form})
