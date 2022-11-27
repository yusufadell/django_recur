# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Issue, PostCategory, Post


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



    actions = (
        "hide_post",
        "make_post_visible",
    )

    def hide_post(self, request, queryset):
        updated = queryset.update(is_visible=False)
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully marked {updated} post(s) as hidden",
        )

    hide_post.short_description = "Hide posts from issue"

    def make_post_visible(self, request, queryset):
        updated = queryset.update(is_visible=True)
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully made {updated} post(s) visible",
        )

    make_post_visible.short_description = "Make posts visible"


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
    )
    search_fields = ("name",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email_address",
        "subscribed",
        "verified",
        "token_expired",
        "verification_sent_date",
    )
    list_filter = (
        "subscribed",
        "verified",
        "verification_sent_date",
    )
    search_fields = ("email_address",)
    date_hierarchy = "created_at"
    exclude = ("token",)
