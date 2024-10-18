# Generated by Django 5.0.1 on 2024-10-18 11:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0003_alter_department_name"),
        ("employees", "0006_educationtransaction"),
        ("job_subtypes", "0003_alter_jobsubtype_name"),
        ("positions", "0004_alter_position_options_position_order"),
        ("statuses", "0002_alter_status_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployeeProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("employees.employee",),
        ),
        migrations.AlterModelOptions(
            name="employee",
            options={"ordering": ["firstname"]},
        ),
        migrations.RemoveField(
            model_name="employee",
            name="department",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="institution_id",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="job_subtype",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="position",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="salary",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="status",
        ),
        migrations.CreateModel(
            name="Contract",
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
                    "contract_type",
                    models.CharField(
                        choices=[("F", "fulltime"), ("P", "parttime")],
                        default="F",
                        max_length=10,
                    ),
                ),
                (
                    "ownership",
                    models.CharField(
                        choices=[("O", "owner"), ("L", "loaned")],
                        default="O",
                        max_length=10,
                    ),
                ),
                (
                    "salary",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                ("start_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "institution_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^\\d+$", "department id must be numbers only"
                            )
                        ],
                        verbose_name="institution id",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, default="", max_length=1000, verbose_name="notes"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="departments.department",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="employees.employee",
                    ),
                ),
                (
                    "job_subtype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="job_subtypes.jobsubtype",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="positions.position",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="statuses.status",
                    ),
                ),
            ],
        ),
    ]
