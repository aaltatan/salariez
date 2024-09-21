# Generated by Django 5.0 on 2024-09-21 10:09

import django.core.validators
import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cost_centers", "0001_initial"),
        ("departments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="cost_center",
            field=models.ForeignKey(
                help_text="the cost center which belongs to",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="departments",
                to="cost_centers.costcenter",
                verbose_name="cost center",
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="department_id",
            field=models.CharField(
                blank=True,
                default="",
                help_text="if you leave it blank, it will be filled based on parent id serial.",
                max_length=255,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^\\d+$", "department id must be numbers only"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                help_text="parent department if exists.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="children",
                to="departments.department",
            ),
        ),
    ]
