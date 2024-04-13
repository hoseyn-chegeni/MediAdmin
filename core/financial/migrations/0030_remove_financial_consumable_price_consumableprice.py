# Generated by Django 5.0 on 2024-04-13 09:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consumable", "0006_remove_consumablev2_expiration_reminder"),
        ("financial", "0029_financial_doctor"),
        ("reception", "0014_alter_reception_appointment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="financial",
            name="consumable_price",
        ),
        migrations.CreateModel(
            name="ConsumablePrice",
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
                ("price", models.PositiveIntegerField()),
                (
                    "consumable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="consumable.inventory",
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="financial.financial",
                    ),
                ),
                (
                    "reception",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reception.reception",
                    ),
                ),
            ],
        ),
    ]
