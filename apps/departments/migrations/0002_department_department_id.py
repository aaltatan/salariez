# Generated by Django 5.0 on 2024-09-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="department",
            name="department id",
            field=models.CharField(default="", max_length=255, unique=True),
        ),
    ]
