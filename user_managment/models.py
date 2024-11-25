from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    ROLL_CHOICES = [
        ('Employees', 'Employees'),
        ('Manager', 'Manager'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='main_user')
    role = models.CharField(max_length=50, choices=ROLL_CHOICES)
    data_of_join = models.DateField(null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True, default=0)
    image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    work_hour = models.PositiveIntegerField(default=8)
    is_approved = models.BooleanField(default=False) 

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
    @property
    def calculate_on_hour_billing(self):
        return self.salary / (self.work_hour * 5 * 4)   #(here 4 is weeks in a month,  5 is weekdays in a week)
