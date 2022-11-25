# Generated by Django 3.2.16 on 2022-11-25 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_auto_20221124_1545"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "default_permissions": [],
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.AlterField(
            model_name="associationusers",
            name="has_office_status",
            field=models.BooleanField(default=False, verbose_name="Has office status"),
        ),
        migrations.AlterField(
            model_name="associationusers",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="gdprconsentusers",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                default="", max_length=32, null=True, verbose_name="Phone"
            ),
        ),
    ]
