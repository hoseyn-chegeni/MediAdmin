# Generated by Django 5.0 on 2024-04-05 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0013_equipment_created_at_supplier_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumable",
            name="reoder_quantity",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="consumable",
            name="send_reorder_sms_to_supplier",
            field=models.BooleanField(default=False),
        ),
    ]
