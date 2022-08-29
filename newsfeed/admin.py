from django.contrib import admin, messages
from django.utils import timezone

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
        "is_published",
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
    actions = (
        "publish_issues",
        "make_draft",
    )

    def publish_issues(self, request, queryset):
        updated = queryset.update(is_draft=False)
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully published {updated} issue(s)",
        )

    publish_issues.short_description = "Publish issues now"

    def make_draft(self, request, queryset):
        updated = queryset.update(is_draft=True)
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully marked {updated} issue(s) as draft",
        )

    make_draft.short_description = "Mark issues as draft"


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

    actions = ("send_newsletters",)

    def send_newsletters(self, request, queryset):
        # TODO: Send newsletters to subscribers
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully sent {0} newsletters(s) to subscribers",
        )

    send_newsletters.short_description = "Send newsletters"


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
