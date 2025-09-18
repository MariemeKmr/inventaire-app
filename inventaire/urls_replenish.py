from django.urls import path
from .views_replenish import replenish_index

app_name = "replenish"
urlpatterns = [
    path("", replenish_index, name="index"),
]
