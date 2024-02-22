# Generated by Django 4.2.10 on 2024-02-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
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
                ("case_id", models.CharField(max_length=100)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("fathers_name", models.CharField(max_length=100)),
                ("national_id", models.CharField(max_length=100)),
                ("date_of_birth", models.DateField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                ("phone_number", models.CharField(max_length=15)),
                ("address", models.TextField()),
                (
                    "marital_status",
                    models.CharField(
                        choices=[("S", "Single"), ("M", "Married")], max_length=1
                    ),
                ),
                ("emergency_contact_name", models.CharField(max_length=100)),
                ("emergency_contact_number", models.CharField(max_length=15)),
            ],
        ),
    ]