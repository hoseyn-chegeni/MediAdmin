# Generated by Django 5.0 on 2024-05-06 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planner", "0011_alter_day_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="day",
            name="mock_date",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
