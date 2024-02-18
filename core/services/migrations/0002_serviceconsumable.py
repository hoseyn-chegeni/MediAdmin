# Generated by Django 4.2.10 on 2024-02-17 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceConsumable",
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
                ("dose", models.CharField(blank=True, max_length=10, null=True)),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "consumable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="asset.consumable",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="services.service",
                    ),
                ),
            ],
        ),
    ]