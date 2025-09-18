from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="/admin/login/")
def history_index(request):
    return render(request, "history/index.html")
