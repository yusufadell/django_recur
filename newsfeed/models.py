import uuid

from django.db import models
from django.urls import reverse

from newsfeed.managers import (
    CustomIssueManager,
    CustomPostManager,
    CustomSubscriberManager,
)


class Issue(models.Model):
    class Interval(models.TextChoices):
        DAILY_ISSUE = "1", "Daily Issue"
        WEEKLY_ISSUE = "2", "Weekly Issue"
        MONTHLY_ISSUE = "3", "Monthly Issue"

    title = models.CharField(max_length=128)
    issue_number = models.PositiveIntegerField(
        unique=True, help_text="Used as a slug for each issue"
    )
    publish_date = models.DateTimeField()
    issue_type = models.CharField(
        max_length=1,
        choices=Interval.choices,
        default=Interval.WEEKLY_ISSUE,
    )
    short_description = models.TextField(blank=True, null=True)
    is_draft = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomIssueManager()

    class Meta:
        ordering = ["-publish_date", "-issue_number"]
        indexes = [models.Index(fields=["publish_date", "issue_number"])]

    def get_absolute_url(self):
        return reverse(
            "newsfeed:issue_detail",
            kwargs={"issue_number": self.issue_number},
        )

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Post categories"
        ordering = ["order"]
        indexes = [models.Index(fields=["order"])]


class Post(models.Model):
    issue = models.ForeignKey(
        Issue,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255)
    source_url = models.URLField()
    is_visible = models.BooleanField(default=True)
    short_description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomPostManager()

    class Meta:
        ordering = ["order", "-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "issue",
                    "category",
                    "order",
                    "-created_at",
                ],
            )
        ]

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="newsletters",
    )
    subject = models.CharField(max_length=128)
    schedule = models.DateTimeField(blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-schedule"]
        indexes = [models.Index(fields=["-schedule"])]

    def __str__(self):
        return self.subject


class Subscriber(models.Model):
    email_address = models.EmailField(unique=True)
    token = models.UUIDField(max_length=128, unique=True, default=uuid.uuid4)
    verified = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)
    verification_sent_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomSubscriberManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["-created_at"])]

    def __str__(self):
        return self.email_address
