# Generated by Django 5.0 on 2024-05-24 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0021_alter_equipment_last_maintenance_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Consumable",
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
                ("name", models.TextField()),
            ],
        ),
    ]