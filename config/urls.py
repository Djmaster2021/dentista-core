# config/urls.py
from django.contrib import admin
from django.urls import include, path
from apps.accounts import urls as accounts_urls
from apps.accounts.views import root_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_redirect, name="root"),
    path("", include((accounts_urls.webpatterns, "accounts"), namespace="accounts")),
    path('accounts/', include('allauth.urls')),
]
