# Generated by Django 5.0 on 2024-04-30 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0013_alter_client_case_id"),
        ("planner", "0005_alter_session_national_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="session",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="client.client",
            ),
        ),
    ]