# Generated by Django 3.2.16 on 2023-03-07 13:17

import datetime

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import plana.apps.documents.models.document
import plana.apps.documents.models.document_association_user
import plana.storages


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('associations', '0030_association_can_submit_projects'),
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
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
                (
                    'description',
                    models.TextField(default='', verbose_name='Description'),
                ),
                ('contact', models.TextField(verbose_name='Contact address')),
                (
                    'is_multiple',
                    models.BooleanField(default=False, verbose_name='Is multiple'),
                ),
                (
                    'days_before_expiration',
                    models.DurationField(
                        default=datetime.timedelta(days=365),
                        verbose_name='Days before document expiration',
                    ),
                ),
                (
                    'path_template',
                    plana.storages.DynamicStorageFileField(
                        blank=True,
                        null=True,
                        upload_to=plana.apps.documents.models.document.get_template_path,
                        verbose_name='Example template file',
                    ),
                ),
                (
                    'mime_types',
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        default=list,
                        size=None,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='DocumentAssociationUser',
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
                    'upload_date',
                    models.DateTimeField(auto_now_add=True, verbose_name='Upload date'),
                ),
                (
                    'path_file',
                    plana.storages.DynamicStorageFileField(
                        upload_to=plana.apps.documents.models.document_association_user.get_file_path,
                        verbose_name='Uploaded file',
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('DOCUMENT_REJECTED', 'Document Rejected'),
                            ('DOCUMENT_PROCESSING', 'Document Processing'),
                            ('DOCUMENT_VALIDATED', 'Document Validated'),
                        ],
                        default='DOCUMENT_PROCESSING',
                        max_length=32,
                        verbose_name='Status',
                    ),
                ),
                (
                    'association',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to='associations.association',
                        verbose_name='Association',
                    ),
                ),
                (
                    'document',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to='documents.document',
                        verbose_name='Document',
                    ),
                ),
                (
                    'project',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to='projects.project',
                        verbose_name='Project',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='User',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Document from association or user',
                'verbose_name_plural': 'Documents from associations or users',
            },
        ),
    ]