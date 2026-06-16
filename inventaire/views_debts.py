from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import Dette, PaiementDette, Historique, Utilisateur
from .views_sales import _get_or_create_utilisateur


def _enrich_debt(d):
    total_paye = d.paiementdette_set.aggregate(s=Sum("montant"))["s"] or 0
    restant = d.montant - total_paye
    return {
        "id": d.id,
        "nom_client": d.nom_client,
        "telephone": d.telephone,
        "montant": d.montant,
        "total_paye": total_paye,
        "restant": max(restant, 0),
        "statut": d.statut,
        "date_dette": d.date_dette,
        "produits_txt": d.produits_txt,
        "remarques": d.remarques,
        "is_late": restant > 0 and (timezone.now().date() - d.date_dette).days > 30,
    }


# ── Liste ──────────────────────────────────────────────────────────────
@login_required
def debt_list(request):
    qs = Dette.objects.order_by("-date_dette")

    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    date_from = request.GET.get("from", "")
    date_to = request.GET.get("to", "")
    late = request.GET.get("late", "")

    if q:
        qs = qs.filter(Q(nom_client__icontains=q) | Q(telephone__icontains=q))
    if status:
        qs = qs.filter(statut=status)
    if date_from:
        qs = qs.filter(date_dette__gte=date_from)
    if date_to:
        qs = qs.filter(date_dette__lte=date_to)

    debts = [_enrich_debt(d) for d in qs]

    if late:
        debts = [d for d in debts if d["is_late"]]

    # Totaux
    totals = {
        "du":      sum(d["montant"]    for d in debts),
        "paye":    sum(d["total_paye"] for d in debts),
        "restant": sum(d["restant"]    for d in debts),
    }

    paginator = Paginator(debts, 20)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    ctx = {
        "debts": page_obj,
        "page_obj": page_obj,
        "totals": totals,
        "filters": {"q": q, "status": status, "from": date_from, "to": date_to, "late": late},
    }
    return render(request, "debts/list.html", ctx)


# ── Détail ─────────────────────────────────────────────────────────────
@login_required
def debt_detail(request, id):
    d = get_object_or_404(Dette, pk=id)
    debt = _enrich_debt(d)
    payments = d.paiementdette_set.order_by("-date_paiement").values(
        "montant", "date_paiement"
    )
    ctx = {
        "debt": debt,
        "payments": payments,
        "total_paye": debt["total_paye"],
    }
    return render(request, "debts/detail.html", ctx)


# ── Nouvelle dette ─────────────────────────────────────────────────────
@login_required
def debt_new(request):
    if request.method == "POST":
        nom_client  = request.POST.get("nom_client", "").strip()
        telephone   = request.POST.get("telephone", "").strip() or None
        montant     = request.POST.get("montant")
        date_dette  = request.POST.get("date_dette")
        statut      = request.POST.get("statut", "EN_COURS")
        produits_txt = request.POST.get("produits_txt", "").strip() or None
        remarques   = request.POST.get("remarques", "").strip() or None

        if not nom_client or not montant or not date_dette:
            messages.error(request, "Nom, montant et date sont obligatoires.")
            return render(request, "debts/form.html", {"mode": "new", "form": request.POST})

        with transaction.atomic():
            dette = Dette.objects.create(
                nom_client=nom_client,
                telephone=telephone,
                montant=montant,
                date_dette=date_dette,
                statut=statut,
                produits_txt=produits_txt,
                remarques=remarques,
            )
            utilisateur = _get_or_create_utilisateur(request.user)
            Historique.objects.create(
                type_action="DETTE_CREEE",
                utilisateur=utilisateur,
                utilisateur_email=request.user.email,
                description=f"Dette créée : {nom_client} — {montant} FCFA",
                date_action=timezone.now(),
            )

        messages.success(request, f"Dette de {nom_client} créée.")
        return redirect("debts:detail", id=dette.id)

    ctx = {"mode": "new", "form": {}, "today": timezone.now().date().isoformat()}
    return render(request, "debts/form.html", ctx)


# ── Modifier ───────────────────────────────────────────────────────────
@login_required
def debt_edit(request, id):
    dette = get_object_or_404(Dette, pk=id)

    if request.method == "POST":
        dette.nom_client   = request.POST.get("nom_client", "").strip()
        dette.telephone    = request.POST.get("telephone", "").strip() or None
        dette.montant      = request.POST.get("montant")
        dette.date_dette   = request.POST.get("date_dette")
        dette.statut       = request.POST.get("statut", "EN_COURS")
        dette.produits_txt = request.POST.get("produits_txt", "").strip() or None
        dette.remarques    = request.POST.get("remarques", "").strip() or None
        dette.save()
        messages.success(request, "Dette mise à jour.")
        return redirect("debts:detail", id=dette.id)

    form = {
        "nom_client":   dette.nom_client,
        "telephone":    dette.telephone or "",
        "montant":      dette.montant,
        "date_dette":   dette.date_dette.isoformat(),
        "statut":       dette.statut,
        "produits_txt": dette.produits_txt or "",
        "remarques":    dette.remarques or "",
    }
    ctx = {"mode": "edit", "form": form, "dette": dette}
    return render(request, "debts/form.html", ctx)


# ── Supprimer ──────────────────────────────────────────────────────────
@login_required
def debt_delete(request, id):
    dette = get_object_or_404(Dette, pk=id)
    debt = _enrich_debt(dette)

    if request.method == "POST":
        dette.delete()
        messages.success(request, "Dette supprimée.")
        return redirect("debts:list")

    return render(request, "debts/confirm_delete.html", {"debt": debt})


# ── Ajouter paiement ───────────────────────────────────────────────────
@login_required
def debt_pay(request, id):
    dette = get_object_or_404(Dette, pk=id)
    debt = _enrich_debt(dette)

    if request.method == "POST":
        montant_str = request.POST.get("montant", "")
        try:
            montant = float(montant_str)
        except ValueError:
            messages.error(request, "Montant invalide.")
            return redirect("debts:pay", id=id)

        if montant <= 0:
            messages.error(request, "Le montant doit être positif.")
            return redirect("debts:pay", id=id)

        if montant > float(debt["restant"]):
            messages.error(request, f"Le montant dépasse le restant ({debt['restant']:,.0f} FCFA).")
            return redirect("debts:pay", id=id)

        with transaction.atomic():
            PaiementDette.objects.create(
                dette=dette,
                montant=montant,
                date_paiement=timezone.now(),
            )
            # Recalcul statut
            nouveau_total = float(debt["total_paye"]) + montant
            if nouveau_total >= float(dette.montant):
                dette.statut = "PAYEE"
            elif nouveau_total > 0:
                dette.statut = "PARTIEL"
            dette.save(update_fields=["statut"])

            utilisateur = _get_or_create_utilisateur(request.user)
            Historique.objects.create(
                type_action="PAIEMENT_DETTE",
                utilisateur=utilisateur,
                utilisateur_email=request.user.email,
                description=f"Paiement {montant:,.0f} FCFA sur dette #{dette.id} ({dette.nom_client})",
                date_action=timezone.now(),
            )

        messages.success(request, f"Paiement de {montant:,.0f} FCFA enregistré.")
        return redirect("debts:detail", id=id)

    ctx = {
        "debt": debt,
        "form": {"date_paiement": timezone.now().strftime("%Y-%m-%dT%H:%M")},
    }
    return render(request, "debts/pay_form.html", ctx)


# ── Historique paiements ───────────────────────────────────────────────
@login_required
def debt_payments(request, id):
    dette = get_object_or_404(Dette, pk=id)
    debt = _enrich_debt(dette)
    payments = dette.paiementdette_set.order_by("-date_paiement")
    ctx = {"debt": debt, "payments": payments, "total_paye": debt["total_paye"]}
    return render(request, "debts/payments.html", ctx)
