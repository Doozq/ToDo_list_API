# Generated by Django 5.1.3 on 2024-11-19 15:02

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "Новая"),
                            ("IN_WORK", "В работе"),
                            ("DONE", "Выполнена"),
                            ("CANCELED", "Отменена"),
                        ],
                        default="NEW",
                        max_length=9,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]