from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms_products import ProductForm

@login_required()
def list_products(request):
    q = (request.GET.get("q") or "").strip().lower()

    # --- DEMO TEMPORAIRE (à remplacer par requêtes ORM) ---
    categories = [
        {"id": 1, "nom": "Parfums"},
        {"id": 2, "nom": "Encens"},
        {"id": 3, "nom": "Brumes"},
    ]
    products = [
        {"id": 101, "nom": "Musc Blanc", "prix_vente": 5000, "quantite": 3, "image_url": "https://via.placeholder.com/300x200?text=Musc", "categorie": categories[0]},
        {"id": 102, "nom": "Oud Royal", "prix_vente": 12000, "quantite": 10, "image_url": "https://via.placeholder.com/300x200?text=Oud", "categorie": categories[0]},
        {"id": 201, "nom": "Encens Bakhoor", "prix_vente": 3000, "quantite": 1, "image_url": "https://via.placeholder.com/300x200?text=Bakhoor", "categorie": categories[1]},
        {"id": 301, "nom": "Brume Vanille", "prix_vente": 3500, "quantite": 8, "image_url": "https://via.placeholder.com/300x200?text=Vanille", "categorie": categories[2]},
    ]
    if q:
        products = [p for p in products if q in p["nom"].lower()]

    class Page: pass
    page_obj = Page()
    page_obj.object_list = products
    # --- FIN DEMO ---

    ctx = {
        "categories": categories,
        "page_obj": page_obj,
        "low_stock_threshold": 3,
    }
    return render(request, "products/list.html", ctx)

@login_required()
def new_product(request):
    """
    Stub MVP:
    - Affiche le formulaire
    - Valide les règles (pv > pa)
    - TODO backend (Idrissa):
        * Traiter image_file -> Remove.bg -> Cloudinary -> image_url
        * Créer Catégorie si nécessaire
        * Créer Produit (ORM) puis rediriger vers products:list
        * Log Historique (produit_ajout)
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # PLACEHOLDER: ici on ne persiste pas encore (attend le backend)
            cd = form.cleaned_data
            messages.success(request, f"Produit “{cd.get('nom')}” prêt à être créé (stub).")
            return redirect("products:list")
        else:
            messages.error(request, "Corrige les erreurs du formulaire.")
    else:
        form = ProductForm()

    return render(request, "products/new.html", {"form": form})

