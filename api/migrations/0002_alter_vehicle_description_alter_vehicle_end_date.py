# Generated by Django 5.1.4 on 2024-12-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
