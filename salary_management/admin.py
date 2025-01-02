from django.contrib import admin
from .models import SalarySlips
# Register your models here.

@admin.register(SalarySlips)
class AdminSalarySilps(admin.ModelAdmin):
    list_display = ['month_year', 'disbursed_salary', 'salary_pdf']