# Generated by Django 3.2.16 on 2022-11-14 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_remove_user_is_cas"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "default_permissions": [],
                "verbose_name": "Utilisateur",
                "verbose_name_plural": "Utilisateurs",
            },
        ),
        migrations.AlterField(
            model_name="associationusers",
            name="has_office_status",
            field=models.BooleanField(default=False, verbose_name="Membre du bureau ?"),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(default="", max_length=25, verbose_name="Téléphone"),
        ),
    ]