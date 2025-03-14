# Generated by Django 5.1.7 on 2025-03-09 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
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
                ("updated_at", models.DateTimeField(auto_created=True, auto_now=True)),
                (
                    "created_at",
                    models.DateTimeField(auto_created=True, auto_now_add=True),
                ),
                ("title", models.CharField(max_length=256)),
                ("content", models.TextField()),
            ],
            options={
                "db_table": "blog",
            },
        ),
        migrations.CreateModel(
            name="Blogfile",
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
                ("bid", models.BigIntegerField()),
                ("file", models.JSONField()),
            ],
            options={
                "db_table": "blogfile",
            },
        ),
    ]
