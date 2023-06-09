# Generated by Django 3.2.16 on 2023-03-07 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0002_institution_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('acronym', models.CharField(max_length=30, verbose_name='Acronym')),
                (
                    'institution',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to='institutions.institution',
                        verbose_name='Institution',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Commission',
                'verbose_name_plural': 'Commissions',
            },
        ),
        migrations.CreateModel(
            name='CommissionDate',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'submission_date',
                    models.DateField(verbose_name='Project submission limit date'),
                ),
                ('commission_date', models.DateField(verbose_name='Commission date')),
                (
                    'commission',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to='commissions.commission',
                        verbose_name='Commission',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Commission Date',
                'verbose_name_plural': 'Commissions Dates',
            },
        ),
    ]
