from django.urls import path
from .views_sales import quick_sale

app_name = "sales"
urlpatterns = [
    path("quick/", quick_sale, name="quick"),
]
