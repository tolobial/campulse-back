# Generated by Django 3.2.16 on 2023-03-30 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_institution_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='email',
        ),
    ]
