# Generated by Django 4.2.10 on 2024-03-11 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financial", "0010_alter_financial_payment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financial",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("پرداخت شده", "پرداخت شده"),
                    ("پرداخت نشده", "پرداخت نشده"),
                    ("اقساط", "اقساط"),
                ],
                default="پرداخت نشده",
                max_length=20,
            ),
        ),
    ]
