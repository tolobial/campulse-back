# Generated by Django 3.2.16 on 2023-05-25 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('associations', '0035_auto_20230525_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='country',
            field=models.CharField(default='', max_length=128, verbose_name='Country'),
        ),
    ]