# Generated by Django 5.0 on 2024-09-22 14:31

import django.core.validators
import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                4,
                                "name of the faculty should not be less than 4 characters.",
                            )
                        ],
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, default="", max_length=255),
                ),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "search",
                    models.GeneratedField(
                        db_persist=False,
                        expression=django.db.models.functions.text.Concat(
                            models.F("name"), models.Value(" "), models.F("name")
                        ),
                        output_field=models.CharField(max_length=255),
                    ),
                ),
                (
                    "has_salary",
                    models.BooleanField(
                        default=False,
                        help_text="can he has a salary?",
                        verbose_name="has salary",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "statuses",
                "ordering": ["name"],
                "permissions": [["can_export", "Can export data"]],
            },
        ),
    ]
