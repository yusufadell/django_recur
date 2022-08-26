# Generated by Django 4.0.6 on 2022-08-26 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_type',
            field=models.PositiveSmallIntegerField(choices=[('1', 'Daily Issue'), ('2', 'Weekly Issue'), ('4', 'Weekly Issue')], default='2'),
        ),
    ]
