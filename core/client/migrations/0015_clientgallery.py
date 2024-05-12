# Generated by Django 5.0 on 2024-05-12 07:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0014_client_initial_session"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientGallery",
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
                ("image", models.ImageField(upload_to="images")),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="client.client"
                    ),
                ),
            ],
        ),
    ]
