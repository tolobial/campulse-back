# Generated by Django 3.2.16 on 2023-03-21 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0039_alter_groupinstitutioncommissionusers_options'),
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
                        'change_user_all_fields',
                        'Can change can_submit_projects on a user.',
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