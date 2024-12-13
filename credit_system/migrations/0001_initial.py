# Generated by Django 4.2.7 on 2024-12-13 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("customer_id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                (
                    "monthly_salary",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("age", models.IntegerField()),
                (
                    "approved_limit",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "current_debt",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Loan",
            fields=[
                ("loan_id", models.AutoField(primary_key=True, serialize=False)),
                ("loan_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("tenure", models.IntegerField()),
                ("interest_rate", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "monthly_repayment",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("emis_paid_on_time", models.BooleanField(default=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="loans",
                        to="credit_system.customer",
                    ),
                ),
            ],
        ),
    ]