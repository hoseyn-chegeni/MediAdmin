# Generated by Django 4.2.10 on 2024-03-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0019_remove_package_duration_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicepackage",
            name="gap_with_next_service",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
