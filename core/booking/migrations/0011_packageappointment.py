# Generated by Django 4.2.10 on 2024-03-18 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0020_alter_servicepackage_gap_with_next_service"),
        ("client", "0013_alter_client_case_id"),
        ("booking", "0010_appointment_name_appointment_national_code_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PackageAppointment",
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
                (
                    "national_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("date", models.DateField()),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="client.client",
                    ),
                ),
                (
                    "package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="services.package",
                    ),
                ),
            ],
        ),
    ]
