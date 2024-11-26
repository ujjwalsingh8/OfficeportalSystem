from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SalarySlips(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month_year = models.CharField(max_length=120)
    disbursed_salary = models.PositiveIntegerField(default=0)
    salary_pdf =models.FileField(upload_to='salary_slips/')