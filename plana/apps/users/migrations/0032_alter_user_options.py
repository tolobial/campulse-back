# Generated by Django 3.2.16 on 2023-02-27 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20230214_1400'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={
                'permissions': [
                    ('add_user_misc', 'Can add a user with no association linked.'),
                    (
                        'change_user_misc',
                        'Can change a user with no association linked.',
                    ),
                    (
                        'delete_user_misc',
                        'Can delete a user with no association linked.',
                    ),
                    ('view_user_misc', 'Can view a user with no association linked.'),
                    ('view_user_anyone', 'Can view all users.'),
                ],
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
