# Generated by Django 4.2.7 on 2024-12-13 12:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("credit_system", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="emis_paid_on_time",
            field=models.IntegerField(default=0),
        ),
    ]
