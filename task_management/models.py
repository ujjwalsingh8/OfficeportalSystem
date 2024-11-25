from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):   

    TASK_CHOICES = [
        ('Pending', 'Pending'),
        ('In_Progress', 'In Progress'),
        ('Done', 'Done'),
    ]
    
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_by')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")
    task_title = models.CharField(max_length=100)
    task_description = models.TextField()
    status = models.CharField(max_length=20, choices=TASK_CHOICES, default='Pending')
    comment = models.TextField()

    def __str__(self):
        return self.task_title 
    