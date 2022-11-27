# Generated by Django 4.1.3 on 2022-11-27 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Issue",
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
                ("title", models.CharField(max_length=128)),
                (
                    "issue_number",
                    models.PositiveIntegerField(
                        help_text="Used as a slug for each issue", unique=True
                    ),
                ),
                ("publish_date", models.DateTimeField()),
                (
                    "issue_type",
                    models.CharField(
                        choices=[
                            ("1", "Daily Issue"),
                            ("2", "Weekly Issue"),
                            ("3", "Monthly Issue"),
                        ],
                        default="2",
                        max_length=1,
                    ),
                ),
                ("short_description", models.TextField(blank=True, null=True)),
                ("is_draft", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-publish_date", "-issue_number"],
            },
        ),
    ]
