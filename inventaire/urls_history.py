from django.urls import path
from .views_history import history_index

app_name = "history"
urlpatterns = [
    path("", history_index, name="index"),
]
