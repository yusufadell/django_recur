from django.db import models
from django.utils import timezone


class IssueQuerySet(models.QuerySet):
    def released(self):
        return self.annotate(
            released=models.Case(
                models.When(
                    is_draft=False, publish_date__lte=timezone.now(), then=True
                ),
                default=False,
                output_field=models.BooleanField(),
            )
        )

    def drafts(self):
        return self.released().filter(released=False)

    def published(self):
        return self.released().filter(released=True)

    def latest_issue(self):
        return self.published().latest("publish_date")


# manager from query set
class CustomIssueManager(models.Manager.from_queryset(IssueQuerySet)):
    pass


class PostQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(is_visible=True)

    def hidden(self):
        return self.filter(is_visible=False)


class CustomPostManager(models.Manager.from_queryset(PostQuerySet)):
    pass


class SubscriberQuerySet(models.QuerySet):
    def subscribed(self):
        self.annotate(subscribed=models.Case(subscribed=True))


class CustomSubscriberManager(models.Manager.from_queryset(SubscriberQuerySet)):
    pass
