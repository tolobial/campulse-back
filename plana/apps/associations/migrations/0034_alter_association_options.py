# Generated by Django 3.2.16 on 2023-04-18 12:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('associations', '0033_auto_20230418_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='association',
            options={
                'permissions': [
                    (
                        'add_association_any_institution',
                        'Can create an association from any institution.',
                    ),
                    (
                        'add_association_all_fields',
                        'Can create an association with is_public setting.',
                    ),
                    (
                        'change_association_any_institution',
                        'Can change fields for an association from any institution.',
                    ),
                    (
                        'change_association_all_fields',
                        'Can change restricted fields for an association.',
                    ),
                    (
                        'delete_association_any_institution',
                        'Can delete an association from any institution.',
                    ),
                    (
                        'view_association_not_enabled',
                        'Can view a not enabled association.',
                    ),
                    (
                        'view_association_not_public',
                        'Can view a not public association.',
                    ),
                ],
                'verbose_name': 'Association',
                'verbose_name_plural': 'Associations',
            },
        ),
    ]
