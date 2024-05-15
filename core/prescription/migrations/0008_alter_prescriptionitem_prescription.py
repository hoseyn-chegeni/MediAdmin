# Generated by Django 5.0 on 2024-05-14 06:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prescription", "0007_temporaryprescription"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prescriptionitem",
            name="prescription",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="prescription.temporaryprescription",
            ),
        ),
    ]