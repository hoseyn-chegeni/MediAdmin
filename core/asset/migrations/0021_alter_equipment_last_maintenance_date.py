# Generated by Django 5.0 on 2024-05-18 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0020_alter_equipment_acquisition_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipment",
            name="last_maintenance_date",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]