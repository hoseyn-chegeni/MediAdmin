# Generated by Django 5.0 on 2024-04-13 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financial", "0035_financial_consumable_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="financial",
            name="tax",
        ),
        migrations.AddField(
            model_name="financial",
            name="consumable_price_final",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="financial",
            name="consumable_tax",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="financial",
            name="service_price_final",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="financial",
            name="service_tax",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
