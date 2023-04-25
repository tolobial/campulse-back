# Generated by Django 3.2.16 on 2023-04-24 10:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0011_auto_20230424_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='other_email',
            field=models.EmailField(
                default='', max_length=150, null=True, verbose_name='Other email'
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='other_first_name',
            field=models.CharField(
                default='', max_length=150, null=True, verbose_name='Other first name'
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='other_last_name',
            field=models.CharField(
                default='', max_length=150, null=True, verbose_name='Other last name'
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='other_phone',
            field=models.CharField(
                default='', max_length=32, null=True, verbose_name='Other phone'
            ),
        ),
    ]