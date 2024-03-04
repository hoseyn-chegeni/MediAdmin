# Generated by Django 4.2.10 on 2024-02-25 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0003_service_doctor"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="recommendations",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="service",
            name="therapeutic_measures",
            field=models.TextField(blank=True),
        ),
    ]