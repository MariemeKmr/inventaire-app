from datetime import date, timedelta
from django.db.models import Sum
from django.utils.timezone import now
from django.shortcuts import render

# adapte ces imports selon tes modèles
from inventaire.models import Produit, Vente, Dette

def dashboard(request):
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)

    # KPIs (adapte les noms de champs)
    kpi_today = Vente.objects.filter(date__date=today).aggregate(s=Sum("total"))["s"] or 0
    kpi_week  = Vente.objects.filter(date__date__gte=start_week).aggregate(s=Sum("total"))["s"] or 0
    kpi_month = Vente.objects.filter(date__date__gte=start_month).aggregate(s=Sum("total"))["s"] or 0

    # Stock faible (ex: stock <= seuil)
    low_stock = Produit.objects.filter(stock__lte=F("seuil")).order_by("stock")[:8]

    # Ventes récentes (adapte les champs)
    recent = (
        Vente.objects.order_by("-date")
        .values("date", "product__name", "qty", "total")[:10]
    )
    recent = [
        {
            "date": r["date"],
            "product_name": r["product__name"],
            "qty": r["qty"],
            "total": r["total"],
        }
        for r in recent
    ]

    debts_open = Dette.objects.filter(status="open").count()

    ctx = {
        "kpi_today_revenue": kpi_today,
        "kpi_week_revenue": kpi_week,
        "kpi_month_revenue": kpi_month,
        "debts_open_count": debts_open,
        "low_stock_products": low_stock,
        "recent_sales": recent,
    }
    return render(request, "core/dashboard.html", ctx)
