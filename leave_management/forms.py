from django import forms
from leave_management.models import LeaveAppication


class LeaveApplicationsForm(forms.ModelForm):
    class Meta:
       model = LeaveAppication
       fields = ['leave_type', 'start_date', 'end_date']
