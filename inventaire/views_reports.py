# views_reports.py
from django.db.models import Sum
from .models import StockQuant, StockMove
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def stock_on_hand(request):
    quants = (StockQuant.objects
              .select_related("product","location")
              .order_by("product__name"))
    return render(request, "reports/stock_on_hand.html", {"quants": quants})

@login_required
def stock_ledger(request):
    moves = (StockMove.objects
             .select_related("product","location")
             .order_by("-date"))
    # TODO: filtres GET: ?product=...&date_from=...&date_to=...
    return render(request, "reports/stock_ledger.html", {"moves": moves})
