# Generated by Django 4.2.10 on 2024-03-22 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0005_alter_doctor_image"),
        ("financial", "0028_financial_doctors_wage_financial_revenue"),
    ]

    operations = [
        migrations.AddField(
            model_name="financial",
            name="doctor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="doctor.doctor",
            ),
        ),
    ]
