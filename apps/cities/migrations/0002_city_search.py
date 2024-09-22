# Generated by Django 5.0 on 2024-09-22 04:00

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cities", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="search",
            field=models.GeneratedField(
                db_persist=False,
                expression=django.db.models.functions.text.Concat(
                    models.F("name"), models.Value(" "), models.F("name")
                ),
                output_field=models.CharField(max_length=255),
            ),
        ),
    ]
