# Generated by Django 5.0 on 2024-04-13 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0036_alter_serviceconsumable_consumable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="price",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
