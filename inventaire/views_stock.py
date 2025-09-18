# views_stock.py (fonctions simples)
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import PurchaseOrder, SalesOrder, StockMove

@login_required
def po_list(request):
    pos = PurchaseOrder.objects.order_by("-created_at")
    return render(request, "stock/po_list.html", {"pos": pos})

@permission_required("app.change_purchaseorder")
def po_receive(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == "POST":
        # TODO: lire les quantités reçues du formulaire, créer StockMove IN
        # StockMove.objects.create(product=..., qty=..., location=..., move_type="IN", ref=po.number)
        po.status = "received"
        po.save()
        return redirect("po_detail", pk=po.pk)
    return render(request, "stock/po_receive.html", {"po": po})
