# Generated by Django 5.0 on 2024-04-02 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0018_remove_appointment_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="client_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="packageappointment",
            name="client_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
