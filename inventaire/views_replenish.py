from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms_replenish import ReplenishForm

@login_required(login_url="/admin/login/")
def replenish_index(request):
    """
    MVP (front) :
      - GET: affiche form, pré-sélectionne ?product=<id>
      - POST: valide et affiche success (TODO: brancher ORM: créer mouvement stock, MAJ produit, log)
    """
    # --- DEMO produits (à remplacer par ORM) ---
    demo_products = [
        {"id": 101, "nom": "Musc Blanc"},
        {"id": 102, "nom": "Oud Royal"},
        {"id": 201, "nom": "Encens Bakhoor"},
        {"id": 301, "nom": "Brume Vanille"},
    ]

    if request.method == "POST":
        form = ReplenishForm(request.POST)
        form.set_product_choices(demo_products)
        if form.is_valid():
            cd = form.cleaned_data
            # TODO Backend:
            # - product = Product.objects.get(pk=cd["product"])
            # - StockMovement(type="IN", qty=cd["quantity"], unit_cost=cd["unit_cost"], ...)
            # - product.quantite += qty ; product.prix_achat = unit_cost (optionnel)
            # - Log historique (reappro)
            messages.success(request, f"Réappro OK : +{cd['quantity']} sur le produit #{cd['product']} (stub).")
            return redirect("products:list")
        else:
            messages.error(request, "Corrige les erreurs du formulaire.")
    else:
        form = ReplenishForm()
        form.set_product_choices(demo_products)
        # Pré-selection si ?product=ID
        pid = request.GET.get("product")
        if pid and any(str(p["id"]) == str(pid) for p in demo_products):
            form.initial["product"] = str(pid)

    return render(request, "replenish/index.html", {"form": form})
