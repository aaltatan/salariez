# Generated by Django 5.0.1 on 2024-10-21 22:02

from pathlib import Path

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
    
    # ExchangeRate = apps.get_model('exchange_rates', 'ExchangeRate')
    # qs = ExchangeRate.objects.filter(currency__is_local__exact=True)

    # if not qs.exists():
        
    #     with open(fixtures_path / 'initial_rate.json', 'r') as file:
    #         objects = serializers.deserialize(
    #             'json', file, ignorenonexistent=True
    #         )
    #         for obj in objects:
    #             obj.save()


def delete_initial(apps, schema_editor):
    Klass = apps.get_model('currencies', 'Currency')
    Klass.objects.all().delete()
    # Klass = apps.get_model('exchange_rates', 'ExchangeRate')
    # Klass.objects.all().delete()



class Migration(migrations.Migration):

    dependencies = [
        (
            "currencies",
            "0001_initial_squashed_0002_alter_currency_options_currency_fraction_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="currency",
            name="fraction_name",
            field=models.CharField(max_length=20, verbose_name="fraction name"),
        ),
        migrations.AlterField(
            model_name="currency",
            name="short_name",
            field=models.CharField(max_length=10, verbose_name="short name"),
        ),
        migrations.RunPython(
            create_initial_currency, reverse_code=delete_initial
        ),
    ]
