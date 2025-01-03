# Generated by Django 5.0 on 2024-04-21 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reception", "0014_alter_reception_appointment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reception",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("پرداخت شده", "پرداخت شده"),
                    ("پرداخت نشده", "پرداخت نشده"),
                    ("قسط یندی", "قسط یندی"),
                ],
                max_length=100,
            ),
        ),
    ]
