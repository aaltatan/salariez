# Generated by Django 5.0 on 2024-09-23 15:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cost_centers", "0002_alter_costcenter_options_costcenter_search"),
    ]

    operations = [
        migrations.AlterField(
            model_name="costcenter",
            name="name",
            field=models.CharField(
                max_length=255,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        4, "name of the object should not be less than 4 characters."
                    )
                ],
            ),
        ),
    ]
