from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Dette, Historique, Produit, Utilisateur, Vente

# ──────────────────────────────────────────────
# Helpers panier (stocké en session)
# ──────────────────────────────────────────────
CART_KEY = "cart"


def _get_cart(request):
    """Retourne le dict panier depuis la session : {str(produit_id): qty}"""
    return request.session.get(CART_KEY, {})


def _save_cart(request, cart):
    request.session[CART_KEY] = cart
    request.session.modified = True


def _cart_items_with_products(cart):
    """
    Retourne une liste de dicts enrichis avec les objets Produit.
    Ignore les IDs dont le produit a été supprimé entre-temps.
    """
    if not cart:
        return []
    ids = [int(k) for k in cart]
    products = {p.id: p for p in Produit.objects.filter(id__in=ids)}
    items = []
    for pid_str, qty in cart.items():
        p = products.get(int(pid_str))
        if p:
            items.append({
                "produit": p,
                "qty": qty,
                "unit": p.prix_vente,
                "total": p.prix_vente * qty,
            })
    return items


def _cart_total(items):
    return sum(it["total"] for it in items)


def _get_or_create_utilisateur(user):
    """
    Résout le User Django → Utilisateur métier.
    Crée un Utilisateur métier si absent (premier login).
    """
    obj, _ = Utilisateur.objects.get_or_create(
        email=user.email or f"{user.username}@local",
        defaults={
            "nom": user.get_full_name() or user.username,
            "mot_de_passe": "",
            "is_admin": 1 if user.is_staff else 0,
        },
    )
    return obj


# ──────────────────────────────────────────────
# Vue : Vente rapide (1 produit, 1 clic)
# ──────────────────────────────────────────────
@login_required
def quick_sale(request):
    q = request.GET.get("q", "").strip()
    produits = []
    if q:
        produits = Produit.objects.filter(
            Q(nom__icontains=q) | Q(barcode__icontains=q)
        ).order_by("nom")[:20]

    if request.method == "POST":
        produit_id = request.POST.get("produit_id")
        qty = int(request.POST.get("qty", 1) or 1)
        produit = get_object_or_404(Produit, pk=produit_id)

        if produit.quantite < qty:
            messages.error(request, f"Stock insuffisant pour « {produit.nom} » (dispo : {produit.quantite}).")
            return redirect("sales:quick")

        utilisateur = _get_or_create_utilisateur(request.user)

        with transaction.atomic():
            vente = Vente.objects.create(
                produit=produit,
                quantite=qty,
                total=produit.prix_vente * qty,
                utilisateur=utilisateur,
                user_name_snapshot=request.user.get_full_name() or request.user.username,
            )
            produit.quantite -= qty
            produit.save(update_fields=["quantite"])
            Historique.objects.create(
                type_action="VENTE",
                utilisateur=utilisateur,
                utilisateur_email=request.user.email,
                description=f"Vente rapide : {qty} × {produit.nom} — {vente.total} FCFA",
                date_action=timezone.now(),
            )

        messages.success(request, f"Vente enregistrée : {qty} × {produit.nom}.")
        return redirect("sales:detail", sale_id=vente.id)

    ctx = {"q": q, "produits": produits}
    return render(request, "sales/quick.html", ctx)


# ──────────────────────────────────────────────
# Vue : Panier
# ──────────────────────────────────────────────
@login_required
def cart(request):
    cart = _get_cart(request)
    items = _cart_items_with_products(cart)
    total = _cart_total(items)
    ctx = {"cart_items": items, "cart_total": total}
    return render(request, "sales/cart.html", ctx)


@login_required
@require_POST
def cart_add(request, produit_id):
    """Ajoute ou met à jour la quantité d'un produit dans le panier."""
    produit = get_object_or_404(Produit, pk=produit_id)
    qty = max(1, int(request.POST.get("qty", 1) or 1))
    cart = _get_cart(request)
    key = str(produit_id)
    cart[key] = cart.get(key, 0) + qty
    _save_cart(request, cart)
    messages.success(request, f"« {produit.nom} » ajouté au panier.")
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "products:list"
    return redirect(next_url)


@login_required
@require_POST
def cart_update(request, produit_id):
    """Met à jour la quantité (depuis la page panier)."""
    qty = int(request.POST.get("qty", 0) or 0)
    cart = _get_cart(request)
    key = str(produit_id)
    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = qty
    _save_cart(request, cart)
    return redirect("sales:cart")


@login_required
@require_POST
def cart_remove(request, produit_id):
    cart = _get_cart(request)
    cart.pop(str(produit_id), None)
    _save_cart(request, cart)
    return redirect("sales:cart")


@login_required
@require_POST
def cart_clear(request):
    _save_cart(request, {})
    return redirect("sales:cart")


# ──────────────────────────────────────────────
# Vue : Checkout / Confirmation
# ──────────────────────────────────────────────
@login_required
def checkout(request):
    cart = _get_cart(request)
    items = _cart_items_with_products(cart)
    total = _cart_total(items)

    if not items:
        messages.warning(request, "Votre panier est vide.")
        return redirect("sales:cart")

    if request.method == "POST":
        pay_mode = request.POST.get("paymode", "cash")
        nom_client = request.POST.get("nom_client", "").strip()
        telephone = request.POST.get("telephone", "").strip()
        remarques = request.POST.get("remarques", "").strip()

        # Vérification stock
        for it in items:
            if it["produit"].quantite < it["qty"]:
                messages.error(
                    request,
                    f"Stock insuffisant pour « {it['produit'].nom} » "
                    f"(dispo : {it['produit'].quantite}, demandé : {it['qty']})."
                )
                return redirect("sales:checkout")

        utilisateur = _get_or_create_utilisateur(request.user)
        ventes_ids = []

        with transaction.atomic():
            for it in items:
                p = it["produit"]
                v = Vente.objects.create(
                    produit=p,
                    quantite=it["qty"],
                    total=it["total"],
                    utilisateur=utilisateur,
                    user_name_snapshot=request.user.get_full_name() or request.user.username,
                )
                p.quantite -= it["qty"]
                p.save(update_fields=["quantite"])
                ventes_ids.append(v.id)

            if pay_mode == "debt" and nom_client:
                produits_txt = "; ".join(
                    f"{it['produit'].nom} ×{it['qty']}" for it in items
                )
                Dette.objects.create(
                    nom_client=nom_client,
                    telephone=telephone or None,
                    montant=total,
                    date_dette=timezone.now().date(),
                    produits_txt=produits_txt,
                    remarques=remarques or None,
                    statut="EN_COURS",
                )

            Historique.objects.create(
                type_action="VENTE",
                utilisateur=utilisateur,
                utilisateur_email=request.user.email,
                description=(
                    f"Vente ({len(items)} article(s)) — {total} FCFA"
                    + (f" [Dette: {nom_client}]" if pay_mode == "debt" else "")
                ),
                date_action=timezone.now(),
            )

        _save_cart(request, {})
        messages.success(request, "Vente enregistrée avec succès !")
        # Redirige vers le détail de la première vente du lot
        return redirect("sales:detail", sale_id=ventes_ids[0])

    ctx = {"cart_items": items, "cart_total": total}
    return render(request, "sales/checkout.html", ctx)


# ──────────────────────────────────────────────
# Vue : Historique des ventes
# ──────────────────────────────────────────────
@login_required
def history(request):
    qs = Vente.objects.select_related("produit", "utilisateur").order_by("-date_vente")

    date_from = request.GET.get("from")
    date_to = request.GET.get("to")
    user_q = request.GET.get("user", "").strip()

    if date_from:
        qs = qs.filter(date_vente__date__gte=date_from)
    if date_to:
        qs = qs.filter(date_vente__date__lte=date_to)
    if user_q:
        qs = qs.filter(
            Q(user_name_snapshot__icontains=user_q)
            | Q(utilisateur__nom__icontains=user_q)
        )

    # Pagination légère
    from django.core.paginator import Paginator
    paginator = Paginator(qs, 30)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    # Enrichir avec un résumé texte
    ventes = []
    for v in page_obj:
        ventes.append({
            "id": v.id,
            "date_vente": v.date_vente,
            "resume": f"{v.produit.nom} ×{v.quantite}",
            "total": v.total,
            "utilisateur_nom": v.user_name_snapshot or v.utilisateur.nom,
        })

    ctx = {
        "ventes": ventes,
        "page_obj": page_obj,
        "filters": {"from": date_from, "to": date_to, "user": user_q},
    }
    return render(request, "sales/history.html", ctx)


# ──────────────────────────────────────────────
# Vue : Détail d'une vente
# ──────────────────────────────────────────────
@login_required
def detail(request, sale_id):
    vente = get_object_or_404(
        Vente.objects.select_related("produit", "utilisateur"),
        pk=sale_id,
    )
    items = [{
        "name": vente.produit.nom,
        "qty": vente.quantite,
        "unit": int(vente.produit.prix_vente),
    }]
    ctx = {
        "sale_id": vente.id,
        "sale_date": vente.date_vente.strftime("%d/%m/%Y %H:%M"),
        "seller": vente.user_name_snapshot or vente.utilisateur.nom,
        "items": items,
        "note": "Merci pour votre achat !",
        "vente": vente,
    }
    return render(request, "sales/detail.html", ctx)
