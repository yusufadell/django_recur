from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("newsfeed/", include("newsfeed.urls", namespace="newsfeed")),
]
