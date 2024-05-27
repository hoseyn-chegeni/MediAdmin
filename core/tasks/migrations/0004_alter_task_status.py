# Generated by Django 5.0 on 2024-05-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0003_task_reopen_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("در انتظار بررسی", "در انتظار بررسی"),
                    ("در حال انجام", "در حال انجام"),
                    ("انجام شده", "انجام شده"),
                    ("لغو شده", "لغو شده"),
                    ("توقف کار", "توقف کار"),
                ],
                max_length=100,
            ),
        ),
    ]