from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from .models import Dette, Produit, Vente

LOW_STOCK = 5

@login_required
def dashboard(request):
    now   = timezone.now()
    today = now.date()
    week_start  = today - timezone.timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    def ca(qs): return qs.aggregate(s=Sum("total"))["s"] or 0

    ventes = Vente.objects.all()
    kpi_today_revenue = ca(ventes.filter(date_vente__date=today))
    kpi_week_revenue  = ca(ventes.filter(date_vente__date__gte=week_start))
    kpi_month_revenue = ca(ventes.filter(date_vente__date__gte=month_start))

    debts_open_count = Dette.objects.exclude(statut="PAYEE").count()

    low_stock_products = [
        {"name": p.nom, "category": p.categorie.nom if p.categorie else "—", "stock": p.quantite}
        for p in Produit.objects.select_related("categorie")
                                .filter(quantite__lte=LOW_STOCK)
                                .order_by("quantite")[:8]
    ]

    recent_sales = [
        {"date": v.date_vente, "product_name": v.produit.nom, "qty": v.quantite, "total": int(v.total)}
        for v in Vente.objects.select_related("produit").order_by("-date_vente")[:8]
    ]

    ctx = {
        "kpi_today_revenue": int(kpi_today_revenue),
        "kpi_week_revenue":  int(kpi_week_revenue),
        "kpi_month_revenue": int(kpi_month_revenue),
        "debts_open_count":  debts_open_count,
        "low_stock_products": low_stock_products,
        "recent_sales":      recent_sales,
    }
    return render(request, "core/dashboard.html", ctx)