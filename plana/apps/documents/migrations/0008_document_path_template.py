# Generated by Django 3.2.16 on 2023-03-24 12:48

from django.db import migrations

import plana.apps.documents.models.document
import plana.storages


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_rename_documentassociationuser_documentupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='path_template',
            field=plana.storages.DynamicStorageFileField(
                blank=True,
                null=True,
                upload_to=plana.apps.documents.models.document.get_template_path,
                verbose_name='Example template file',
            ),
        ),
    ]
