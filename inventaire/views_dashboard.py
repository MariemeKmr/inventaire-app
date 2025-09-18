# views_dashboard.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    ctx = {
        "low_stock_count": 0,  # TODO: requêtes réelles
        "to_receive": 0,
        "to_ship": 0,
        "inventory_value": 0,
    }
    return render(request, "core/dashboard.html", ctx)
