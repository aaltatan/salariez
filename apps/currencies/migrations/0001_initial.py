# Generated by Django 5.0.1 on 2024-10-22 10:09

from pathlib import Path

import django.core.validators
import django.db.models.functions.text
from django.db import migrations, models
from django.core import serializers


def create_initial_currency(apps, schema_editor):

    fixtures_path = Path(__file__).resolve().parent.parent / 'fixtures' 

    Currency = apps.get_model('currencies', 'Currency')
    qs = Currency.objects.filter(is_local__exact=True)

    if not qs.exists():
        
        with open(
            fixtures_path / 'initial_currencies.json', 'r'
        ) as file:
            objects = serializers.deserialize(
                'json', file, ignorenonexistent=True
            )
            for obj in objects:
                obj.save()

def delete_initial(apps, schema_editor):
    Currency = apps.get_model('currencies', 'Currency')
    Currency.objects.all().delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Currency",
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
                    "short_name",
                    models.CharField(max_length=10, verbose_name="short name"),
                ),
                (
                    "fraction_name",
                    models.CharField(max_length=20, verbose_name="fraction name"),
                ),
                (
                    "is_local",
                    models.BooleanField(
                        default=False,
                        help_text="is it local or foreign?",
                        verbose_name="is local",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "currencies",
                "ordering": ["is_local", "name"],
                "permissions": [["can_export", "Can export data"]],
            },
        ),
        migrations.RunPython(
            create_initial_currency, reverse_code=delete_initial
        )
    ]