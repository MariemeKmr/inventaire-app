from django.urls import path
from .views_stats import stats_index

app_name = "stats"
urlpatterns = [
    path("", stats_index, name="index"),
]
