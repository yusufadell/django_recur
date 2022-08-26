from django.urls import path

from .views import issue_detail_view, issue_list_view

app_name = "newsfeed"

urlpatterns = [
    path("", issue_list_view, name="issue_list"),
    path("<slug:issue_number>/", issue_detail_view, name="issue_detail"),
]
