# Generated by Django 5.0 on 2024-04-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financial", "0037_alter_financial_payment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financial",
            name="payment_status",
            field=models.CharField(
                choices=[("پرداخت شده", "پرداخت شده"), ("پرداخت نشده", "پرداخت نشده")],
                default="UNPAID",
                max_length=20,
            ),
        ),
    ]
