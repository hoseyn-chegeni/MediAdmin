# Generated by Django 5.0 on 2024-04-03 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0010_supplier_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplier",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]