# Generated by Django 5.0 on 2024-04-05 10:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("type", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("در انتظار بررسی", "در انتظار بررسی"),
                            ("در حال انجام", "در حال انجام"),
                            ("انجام شده", "انجام شده"),
                            ("لغو شده", "لغو شده"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("پایین", "پایین"),
                            ("متوسط", "متوسط"),
                            ("بالا", "بالا"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("answer", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
