# Generated by Django 3.2.16 on 2023-03-06 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0028_auto_20230214_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='charter_status',
            field=models.CharField(
                choices=[
                    ('CHARTER_DRAFT', 'Charter Draft'),
                    ('CHARTER_REJECTED', 'Charter Rejected'),
                    ('CHARTER_PROCESSING', 'Charter Processing'),
                    ('CHARTER_VALIDATED', 'Charter Validated'),
                    ('CHARTER_EXPIRED', 'Charter Expired'),
                ],
                default='CHARTER_DRAFT',
                max_length=32,
                verbose_name='Charter status',
            ),
        ),
        migrations.AlterField(
            model_name='association',
            name='president_phone',
            field=models.CharField(
                default='', max_length=32, verbose_name='President phone'
            ),
        ),
    ]
