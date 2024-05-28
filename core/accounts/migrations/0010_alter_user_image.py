# Generated by Django 4.2.13 on 2024-05-28 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_alter_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(
                blank=True,
                default="app/media/default.png",
                null=True,
                upload_to="images/",
            ),
        ),
    ]