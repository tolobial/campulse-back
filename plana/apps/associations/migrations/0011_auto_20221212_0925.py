# Generated by Django 3.2.16 on 2022-12-12 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("associations", "0010_association_president_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="association",
            name="activity_field",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="associations.activityfield",
                verbose_name="Activity field",
            ),
        ),
        migrations.AlterField(
            model_name="association",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="associations",
                to="associations.institution",
                verbose_name="Institution",
            ),
        ),
        migrations.AlterField(
            model_name="association",
            name="institution_component",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="associations",
                to="associations.institutioncomponent",
                verbose_name="Institution component",
            ),
        ),
    ]
