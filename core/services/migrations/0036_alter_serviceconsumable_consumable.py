# Generated by Django 5.0 on 2024-04-10 12:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consumable", "0001_initial"),
        ("services", "0035_remove_service_inventory_minimum_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serviceconsumable",
            name="consumable",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="consumable.consumablev2",
            ),
        ),
    ]