# Generated by Django 5.0 on 2024-05-08 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0022_delete_appointment"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PackageAppointment",
        ),
    ]
