from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LeaveAppication(models.Model):
    Leave_Type = [
        ('Annual', 'Annual'),
        ('Sick', 'Sick'),
        ('Causal', 'Causal'),
    ]

    Leave_Status = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=Leave_Type)
    leave_status = models.CharField(max_length=50, choices=Leave_Status, default='Pending')
    start_date = models.DateField()
    end_date = models.DateField()
    approved_by = models.ForeignKey(User, related_name='approved_leaves', null=True, on_delete=models.SET_NULL)
