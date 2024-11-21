from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('новая', 'новая'),
        ('в работе', 'в работе'),
        ('выполнена', 'выполнена'),
        ('отменена', 'отменена'),
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='новая')
    file = models.FileField(upload_to='task_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    task = models.ForeignKey(
        'Task', 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)