# Generated by Django 5.0 on 2024-04-13 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financial", "0031_remove_consumableprice_invoice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consumableprice",
            name="reception",
            field=models.PositiveIntegerField(),
        ),
    ]
