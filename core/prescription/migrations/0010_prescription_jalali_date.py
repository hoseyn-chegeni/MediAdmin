# Generated by Django 5.0 on 2024-05-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prescription", "0009_remove_prescription_diagnosis_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="prescription",
            name="jalali_date",
            field=models.CharField(default=1.0, max_length=255),
            preserve_default=False,
        ),
    ]
