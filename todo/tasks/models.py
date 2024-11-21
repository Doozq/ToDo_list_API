from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('IN_WORK', 'В работе'),
        ('DONE', 'Выполнена'),
        ('CANCELED', 'Отменена'),
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='NEW')
    file = models.FileField(upload_to='task_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
