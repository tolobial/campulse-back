# Generated by Django 3.2.16 on 2023-02-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0027_alter_association_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='association',
            name='activities',
        ),
        migrations.RemoveField(
            model_name='association',
            name='description',
        ),
        migrations.AddField(
            model_name='association',
            name='current_projects',
            field=models.TextField(default='', verbose_name='Current projects'),
        ),
        migrations.AddField(
            model_name='association',
            name='social_object',
            field=models.TextField(default='', verbose_name='Social object'),
        ),
    ]
