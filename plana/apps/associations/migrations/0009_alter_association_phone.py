# Generated by Django 3.2.16 on 2022-12-02 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("associations", "0008_association_alt_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="association",
            name="phone",
            field=models.CharField(default="", max_length=32, verbose_name="Phone"),
        ),
    ]
