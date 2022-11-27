import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from newsfeed.managers import CustomIssueManager


class Issue(models.Model):

    class Interval(models.TextChoices):
        DAILY_ISSUE = "1", "Daily Issue"
        WEEKLY_ISSUE = "2", "Weekly Issue"
        MONTHLY_ISSUE = "3", "Monthly Issue"

    title = models.CharField(max_length=128)
    issue_number = models.PositiveIntegerField(
        unique=True, help_text="Used as a slug for each issue")
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
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Post categories"
        ordering = ["order"]
        # indexes = [models.Index(fields=["order"])]


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
        # indexes = [

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

    def __str__(self):
        return self.email_address

    def token_expired(self):
        if not self.verification_sent_date:
            return True

        expiration_date = self.verification_sent_date + timezone.timedelta(
            days=NEWSFEED_EMAIL_CONFIRMATION_EXPIRE_DAYS
        )
        return expiration_date <= timezone.now()

    def reset_token(self):

        unique_token = str(uuid.uuid4())

        while self.__class__.objects.filter(token=unique_token).exists():
            unique_token = str(uuid.uuid4())

        self.token = unique_token
        self.save()

    def subscribe(self):
        if not self.token_expired():
            self.verified = True
            self.subscribed = True
            self.save()

            signals.subscribed.send(sender=self.__class__, instance=self)

            return True

    def unsubscribe(self):
        if self.subscribed:
            self.subscribed = False
            self.verified = False
            self.save()

            signals.unsubscribed.send(sender=Subscriber, instance=self)

            return True

    def send_verification_email(self, created):
        minutes_before = timezone.now() - timezone.timedelta(minutes=5)
        sent_date = self.verification_sent_date

        # Only send email again if the last sent date is five minutes earlier
        if sent_date and sent_date >= minutes_before:
            return

        if not created:
            self.reset_token()

        self.verification_sent_date = timezone.now()
        self.save()

        send_subscription_verification_email(
            self.get_verification_url(), self.email_address
        )
        signals.email_verification_sent.send(sender=self.__class__, instance=self)

    def get_verification_url(self):
        return reverse(
            "newsfeed:newsletter_subscription_confirm", kwargs={"token": self.token}
        )
