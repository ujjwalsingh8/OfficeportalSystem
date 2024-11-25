from django.contrib import admin
from leave_management.models import LeaveAppication
# Register your models here.

@admin.register(LeaveAppication)
class AdminLeave(admin.ModelAdmin):
    list_display = ['id', 'user', 'leave_type', 'leave_status']
