# Generated by Django 5.0 on 2024-05-06 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planner", "0013_remove_deletedsession_reason_deletedsession_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deletedsession",
            name="status",
        ),
        migrations.AddField(
            model_name="deletedsession",
            name="reason",
            field=models.TextField(default="this"),
            preserve_default=False,
        ),
    ]