from django.urls import path
from . import views_debts as views

app_name = "debts"

urlpatterns = [
    path("", views.debt_list, name="list"),
    path("<int:id>/", views.debt_detail, name="detail"),
    path("new/", views.debt_new, name="new"),
    path("<int:id>/edit/", views.debt_edit, name="edit"),
    path("<int:id>/delete/", views.debt_delete, name="delete"),
    path("<int:id>/pay/", views.debt_pay, name="pay"),
    path("<int:id>/payments/", views.debt_payments, name="payments"),
]