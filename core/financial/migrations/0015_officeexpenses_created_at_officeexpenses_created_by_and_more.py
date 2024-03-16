# Generated by Django 4.2.10 on 2024-03-16 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("financial", "0014_officeexpenses_attachment"),
    ]

    operations = [
        migrations.AddField(
            model_name="officeexpenses",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="officeexpenses",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="officeexpenses",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
