# Generated by Django 5.0 on 2024-04-17 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("consumable", "0012_consumablev2_supplier"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="consumablev2",
            name="inventory_tracking_number",
        ),
    ]