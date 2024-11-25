from django.contrib import admin
from leave_management.models import LeaveAppication, CheckInCheckOut, DailyStatus
# Register your models here.

@admin.register(LeaveAppication)
class AdminLeave(admin.ModelAdmin):
    list_display = ['id', 'user', 'leave_type', 'leave_status']


@admin.register(CheckInCheckOut)
class Admincheckin(admin.ModelAdmin):
    list_display = ['id', 'user', 'check_in_time', 'check_out_time', 'total_hours_worked']

@admin.register(DailyStatus)
class AdminDailyStatus(admin.ModelAdmin):
    list_display = ['id', 'report_date', 'status']
