from django import forms
from leave_management.models import LeaveAppication, CheckInCheckOut, DailyStatus


class LeaveApplicationsForm(forms.ModelForm):
    class Meta:
       model = LeaveAppication
       fields = ['leave_type', 'start_date', 'end_date']

class CheckInCheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckInCheckOut
        fields = ['check_in_time', 'check_out_time', 'total_hours_worked']

class DailyStatusForm(forms.ModelForm):
    class Meta:
        model = DailyStatus
        fields = ['report_date', 'status']
