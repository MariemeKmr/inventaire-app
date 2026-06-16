from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("inventaire.urls_accounts", namespace="accounts")),
    path("categories/", include("inventaire.urls_categories", namespace="categories")),
    path("", include("inventaire.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)