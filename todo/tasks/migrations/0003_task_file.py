# Generated by Django 5.1.3 on 2024-11-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_alter_task_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="task_files/"),
        ),
    ]