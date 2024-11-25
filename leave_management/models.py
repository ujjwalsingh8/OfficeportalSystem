from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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


class CheckInCheckOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    total_hours_worked = models.DurationField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True) 

    def __str__(self):
        return f"{self.user.username} -  {self.check_out_time- self.check_in_time}"

    def calculate_total_hours(self):
        self.total_hours_worked = self.check_out_time - self.check_in_time
        self.save()


class DailyStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_date = models.DateTimeField(default=timezone.now)
    status = models.TextField()
