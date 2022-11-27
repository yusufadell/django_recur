from django.db import models
from django.utils import timezone


class IssueQuerySet(models.QuerySet):

    def released(self):
        return self.filter(
            is_draft=False,
            publish_date__lte=timezone.now(),
        )

    def released2(self):
        return self.annotate(
            released=models.Case(
                models.When(
                    is_draft=False, publish_date__lte=timezone.now(), then=True
                ),
                default=False,
                output_field=models.BooleanField(),
            )
        )

# manager from query set
class CustomIssueManager(models.Manager.from_queryset(IssueQuerySet)):
    pass


class PostQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(is_visible=True)

    def hidden(self):
        return self.filter(is_visible=False)

    def number_of_issues(self):
        return self.annotate(number_of_issues=models.Count("issue"))


class CustomPostManager(models.Manager.from_queryset(PostQuerySet)):
    pass


class SubscriberQuerySet(models.QuerySet):
    def subscribed(self):
        self.annotate(subscribed=models.Case(subscribed=True))


class CustomSubscriberManager(models.Manager.from_queryset(SubscriberQuerySet)):
    pass
