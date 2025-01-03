# Generated by Django 5.0 on 2024-05-18 08:11

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planner", "0015_day_christ_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="JalaliDateHandler",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("jalali_date", django_jalali.db.models.jDateField()),
            ],
        ),
    ]
