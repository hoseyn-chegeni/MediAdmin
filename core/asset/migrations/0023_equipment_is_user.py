# Generated by Django 5.0 on 2024-05-26 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0022_consumable"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipment",
            name="is_user",
            field=models.BooleanField(default=False),
        ),
    ]
