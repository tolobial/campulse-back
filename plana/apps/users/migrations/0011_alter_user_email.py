# Generated by Django 3.2.16 on 2022-11-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_alter_user_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]