# Generated by Django 4.2.10 on 2024-03-17 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="national_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
