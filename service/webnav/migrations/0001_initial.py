# Generated by Django 5.1.7 on 2025-03-09 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Webnav",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("weburl", models.CharField(max_length=100)),
                ("imgurl", models.TextField()),
                ("tooltip", models.CharField(max_length=100)),
                ("tag", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "webnav",
            },
        ),
        migrations.CreateModel(
            name="Webnavlabel",
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
                ("tag", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "db_table": "webnavlabel",
            },
        ),
    ]
