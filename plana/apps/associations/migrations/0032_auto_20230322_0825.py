# Generated by Django 3.2.16 on 2023-03-22 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0031_auto_20230309_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='approval_date',
            field=models.DateField(null=True, verbose_name='Approval date'),
        ),
        migrations.AlterField(
            model_name='association',
            name='cga_date',
            field=models.DateField(null=True, verbose_name='CGA date'),
        ),
        migrations.AlterField(
            model_name='association',
            name='last_goa_date',
            field=models.DateField(null=True, verbose_name='Last GOA date'),
        ),
    ]
