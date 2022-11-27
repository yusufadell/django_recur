# Generated by Django 4.1.1 on 2022-11-27 17:48
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("newsfeed", "0002_postcategory_post"),
    ]

    operations = [
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=128)),
                ("schedule", models.DateTimeField(blank=True, null=True)),
                ("is_sent", models.BooleanField(default=False)),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="newsletters",
                        to="newsfeed.issue",
                    ),
                ),
            ],
            options={
                "ordering": ["-schedule"],
            },
        ),
    ]
