from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# NOTE: vues "front-only" (pas de logique métier / DB ici).
# Le backend branchera plus tard sur les modèles + formulaires réels.

@login_required
def debt_list(request):
    # Données démo pour tester le rendu
    debts = [
        {
            "id": 1, "nom_client": "Awa Diop", "telephone": "77 000 00 00",
            "montant": 50000, "total_paye": 20000, "restant": 30000,
            "statut": "PARTIEL", "date_dette": "2025-09-20", "is_late": False,
        },
        {
            "id": 2, "nom_client": "Ibrahima S.", "telephone": None,
            "montant": 15000, "total_paye": 0, "restant": 15000,
            "statut": "EN_COURS", "date_dette": "2025-09-10", "is_late": True,
        },
    ]
    totals = {"du": 65000, "paye": 20000, "restant": 45000}
    ctx = {"debts": debts, "totals": totals}
    return render(request, "debts/list.html", ctx)

@login_required
def debt_detail(request, id):
    debt = {
        "id": id, "nom_client": "Awa Diop", "telephone": "77 000 00 00",
        "montant": 50000, "total_paye": 20000, "restant": 30000,
        "statut": "PARTIEL", "date_dette": "2025-09-20",
        "produits_txt": "Encens x2; Parfum x1", "remarques": "Rappeler lundi"
    }
    payments = [
        {"date_paiement": "2025-09-22 10:15", "montant": 10000, "utilisateur_nom": "Vendeur"},
        {"date_paiement": "2025-09-24 09:03", "montant": 10000, "utilisateur_nom": "Admin"},
    ]
    ctx = {"debt": debt, "payments": payments, "total_paye": 20000}
    return render(request, "debts/detail.html", ctx)

@login_required
def debt_new(request):
    # Front uniquement
    ctx = {"mode": "new", "form": {}}
    return render(request, "debts/form.html", ctx)

@login_required
def debt_edit(request, id):
    # Front uniquement
    form = {
        "nom_client": "Awa Diop", "telephone": "77 000 00 00",
        "montant": 50000, "date_dette": "2025-09-20", "statut": "PARTIEL",
        "produits_txt": "Encens x2; Parfum x1", "remarques": "Rappeler lundi"
    }
    ctx = {"mode": "edit", "form": form}
    return render(request, "debts/form.html", ctx)

@login_required
def debt_delete(request, id):
    debt = {"id": id, "nom_client": "Awa Diop", "montant": 50000}
    return render(request, "debts/confirm_delete.html", {"debt": debt})

@login_required
def debt_pay(request, id):
    debt = {
        "id": id, "nom_client": "Awa Diop",
        "montant": 50000, "total_paye": 20000, "restant": 30000,
    }
    ctx = {"debt": debt, "form": {"date_paiement": ""}}
    return render(request, "debts/pay_form.html", ctx)

@login_required
def debt_payments(request, id):
    debt = {"id": id, "nom_client": "Awa Diop"}
    payments = [
        {"date_paiement": "2025-09-22 10:15", "montant": 10000, "utilisateur_nom": "Vendeur"},
        {"date_paiement": "2025-09-24 09:03", "montant": 10000, "utilisateur_nom": "Admin"},
    ]
    ctx = {"debt": debt, "payments": payments, "total_paye": 20000}
    return render(request, "debts/payments.html", ctx)