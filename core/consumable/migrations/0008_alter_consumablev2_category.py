# Generated by Django 5.0 on 2024-04-15 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consumable", "0007_consumablecategory_alter_consumablev2_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consumablev2",
            name="category",
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
