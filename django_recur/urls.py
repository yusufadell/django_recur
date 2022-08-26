from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", include("newsfeed.urls", namespace="newsfeed")),
]
