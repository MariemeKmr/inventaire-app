from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="/admin/login/")
def list_debts(request):
    return render(request, "debts/list.html")
