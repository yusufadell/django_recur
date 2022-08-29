from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IssueQuerySet(models.QuerySet):

    use_for_related_fields = True

    def released(self):
        return self.filter(is_draft=False, publish_date__lte=timezone.now())


class Issue(TimeStampedModel, models.Model):
    class IssuesInterval(models.TextChoices):
        DAILY_ISSUE = "1", "Daily Issue"
        WEEKLY_ISSUE = "2", "Weekly Issue"
        MONTHLY_ISSUE = "4", "Weekly Issue"

    title = models.CharField(max_length=128)
    issue_number = models.PositiveIntegerField(
        unique=True, help_text="Used as a slug for each issue"
    )
    publish_date = models.DateTimeField()
    issue_type = models.CharField(
        choices=IssuesInterval.choices, max_length=2, default="2"
    )
    short_description = models.TextField(blank=True, null=True)
    is_draft = models.BooleanField(default=False)

    objects = IssueQuerySet.as_manager()

    class Meta:
        ordering = ["-publish_date", "-issue_number"]

    def is_published(self):
        return self.is_draft == False and self.publish_date <= timezone.now()

    def get_absolute_url(self):
        return reverse(
            "newsfeed:issue_detail", kwargs={"issue_number": self.issue_number}
        )

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Post categories"

    def __str__(self):
        return self.name


class Post(TimeStampedModel, models.Model):
    issue = models.ForeignKey(
        Issue, on_delete=models.SET_NULL, related_name="posts", blank=True, null=True
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
    is_visible = models.BooleanField(default=False)
    short_description = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Newsletter(TimeStampedModel, models.Model):
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name="newsletters"
    )
    subject = models.CharField(max_length=128)
    is_sent = models.BooleanField(default=False)
    schedule = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.subject


class Subscriber(TimeStampedModel, models.Model):
    email_address = models.EmailField(unique=True)
    token = models.CharField(max_length=128, unique=True)
    verified = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)
    confirmation_sent_date = models.DateTimeField()

    def __str__(self):
        return self.email_address

    def confirmation_expired(self):
        expiration_date = self.confirmation_sent_date + timezone.timedelta(
            days=settings.SUBSCRIPTION_EMAIL_CONFIRMATION_EXPIRE_DAYS
        )
        return expiration_date <= timezone.now()
