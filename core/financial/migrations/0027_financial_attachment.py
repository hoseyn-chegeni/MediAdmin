# Generated by Django 4.2.10 on 2024-03-21 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financial", "0026_coupon_percentage_alter_coupon_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="financial",
            name="attachment",
            field=models.FileField(blank=True, null=True, upload_to="attachments/"),
        ),
    ]
