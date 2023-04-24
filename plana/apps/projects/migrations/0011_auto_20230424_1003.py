# Generated by Django 3.2.16 on 2023-04-24 08:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0010_auto_20230418_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={
                'permissions': [
                    ('add_project_association', 'Can add a project as an association.'),
                    ('add_project_user', 'Can add a project as a user.'),
                    (
                        'change_project_basic_fields',
                        'Can update projects basic fields.',
                    ),
                    (
                        'change_project_restricted_fields',
                        'Can update projects restricted fields (status, ...).',
                    ),
                    ('view_project_any_commission', 'Can view all projects.'),
                ],
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.AlterModelOptions(
            name='projectcategory',
            options={
                'permissions': [
                    (
                        'view_projectcategory_any_commission',
                        'Can view all categories linked to a project.',
                    )
                ],
                'verbose_name': 'Project category',
                'verbose_name_plural': 'Projects categories',
            },
        ),
        migrations.AlterModelOptions(
            name='projectcomment',
            options={
                'permissions': [
                    (
                        'view_projectcomment_any_commission',
                        'Can view all comments linked to all projects.',
                    )
                ],
                'verbose_name': 'Project comment',
                'verbose_name_plural': 'Projects comments',
            },
        ),
        migrations.AlterModelOptions(
            name='projectcommissiondate',
            options={
                'permissions': [
                    (
                        'change_projectcommissiondate_basic_fields',
                        'Can update basic fields between a project and a commission date.',
                    ),
                    (
                        'change_projectcommissiondate_restricted_fields',
                        'Can update restricted fields (amount earned, ...) between a project and a commission date.',
                    ),
                    (
                        'view_projectcommissiondate_any_commission',
                        'Can view all commission dates linked to a project.',
                    ),
                ],
                'verbose_name': 'Project commission date',
                'verbose_name_plural': 'Projects commissions dates',
            },
        ),
    ]