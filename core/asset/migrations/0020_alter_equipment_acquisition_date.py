# Generated by Django 5.0 on 2024-05-18 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0019_alter_equipment_acquisition_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipment",
            name="acquisition_date",
            field=models.CharField(max_length=255),
        ),
    ]
