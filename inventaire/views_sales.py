from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="/admin/login/")
def quick_sale(request):
    return render(request, "sales/quick.html")


@login_required
def history(request):
    return render(request, "sales/history.html")
@login_required
def detail(request, sale_id):
    return render(request, "sales/detail.html", {"sale_id": sale_id})
@login_required
def cart(request):
    return render(request, "sales/cart.html")
@login_required
def checkout(request):
    return render(request, "sales/checkout.html")

