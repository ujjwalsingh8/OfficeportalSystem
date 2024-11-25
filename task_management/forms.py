from django import forms
from django.contrib.auth.models import User
from task_management.models import Task
from user_managment.models import Profile


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_to', 'task_title', 'task_description']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(main_user__role='Employees')
