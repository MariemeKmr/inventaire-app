from django.urls import path
from .views_debts import list_debts

app_name = "debts"
urlpatterns = [
    path("", list_debts, name="list"),
]
