# Generated by Django 5.0 on 2024-04-11 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consumable", "0002_inventory_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumablev2",
            name="reorder_quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
