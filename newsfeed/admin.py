from django.contrib import admin

from .models import Issue, Newsletter, Post, PostCategory, Subscriber


class PostInline(admin.StackedInline):
    model = Post


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    view_on_site = True
    inlines = (PostInline,)
    date_hierarchy = "publish_date"

    list_display = (
        "title",
        "issue_number",
        "publish_date",
        "issue_type",
        "is_draft",
    )
    list_filter = (
        "is_draft",
        "issue_type",
    )
    search_fields = (
        "title",
        "short_description",
        "posts__title",
        "posts__short_description",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    sortable_by = (
        "issue_number",
        "publish_date",
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_select_related = ("issue",)
    date_hierarchy = "schedule"
    list_display = (
        "subject",
        "issue",
        "is_sent",
        "schedule",
    )
    list_filter = ("is_sent",)
    search_fields = (
        "subject",
        "issue__short_description",
        "issue__title",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    sortable_by = ("schedule",)
    autocomplete_fields = ("issue",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_select_related = (
        "issue",
        "category",
    )
    list_display = (
        "title",
        "category",
        "issue",
        "is_visible",
    )
    list_filter = (
        "is_visible",
        "category",
    )
    search_fields = (
        "title",
        "short_description",
        "issue__title",
        "issue__short_description",
        "category__title",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    autocomplete_fields = (
        "issue",
        "category",
    )


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email_address",
        "subscribed",
        "verified",
        "confirmation_expired",
        "confirmation_sent_date",
    )
    list_filter = (
        "subscribed",
        "verified",
        "confirmation_sent_date",
    )
    search_fields = ("email_address",)
    date_hierarchy = "created_at"
    exclude = ("token",)
