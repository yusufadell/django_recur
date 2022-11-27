# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib import messages

from newsfeed.models import Issue
from newsfeed.models import Newsletter
from newsfeed.models import Post
from newsfeed.models import PostCategory
from newsfeed.models import Subscriber
from newsfeed.utils import send_email_newsletter


class PostInline(admin.StackedInline):
    model = Post
    extra = 0
    raw_id_fields = ("category",)
    classes = ("collapse",)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "issue_number",
        "publish_date",
        "issue_type",
        "short_description",
        "is_draft",
        "created_at",
        "updated_at",
    )
    list_filter = ("publish_date", "is_draft", "created_at", "updated_at")
    date_hierarchy = "created_at"
    search_fields = ("issue_number", "title", "short_description")

    inlines = (PostInline,)
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "order")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "issue",
        "category",
        "title",
        "source_url",
        "is_visible",
        "short_description",
        "order",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "issue",
        "category",
        "is_visible",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    search_fields = ("issue", "title", "source_url", "short_description")
    autocomplete_fields = ("issue", "category")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "issue",
        "subject",
        "schedule",
        "is_sent",
        "sent_at",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "issue",
        "schedule",
        "is_sent",
        "sent_at",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    autocomplete_fields = ("issue",)

    actions = ("send_newsletters",)

    def send_newsletters(self, request, queryset):
        # This should always be overridden to use a task
        send_email_newsletter(newsletters=queryset, respect_schedule=False)
        messages.add_message(
            request,
            messages.SUCCESS,
            "Sending selected newsletters(s) to the subscribers",
        )

    send_newsletters.short_description = "Send newsletters"


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email_address",
        "token",
        "verified",
        "subscribed",
        "verification_sent_date",
        "created_at",
    )
    list_filter = (
        "verified",
        "subscribed",
        "verification_sent_date",
        "created_at",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("token",)
    search_fields = ("email_address",)
