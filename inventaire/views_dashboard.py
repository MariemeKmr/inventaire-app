from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="/admin/login/")
def dashboard(request):
    ctx = {
        "low_stock_count": 0,
        "open_debts_count": 0,
        "revenue_today": "0",
    }
    return render(request, "core/dashboard.html", ctx)
