# Generated by Django 5.0 on 2024-04-06 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0015_rename_reoder_quantity_consumable_reorder_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumable",
            name="expiration_reminder",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
