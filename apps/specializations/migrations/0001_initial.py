# Generated by Django 5.0.1 on 2024-10-15 17:47

import django.core.validators
import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Specialization",
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
                                "name of the object should not be less than 4 characters.",
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
                    "is_specialist",
                    models.BooleanField(
                        default=False,
                        help_text="is it specialist?",
                        verbose_name="is specialist",
                    ),
                ),
            ],
            options={
                "ordering": ["is_specialist", "name"],
                "permissions": [["can_export", "Can export data"]],
            },
        ),
    ]