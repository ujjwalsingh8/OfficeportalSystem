from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLL_CHOICES, required=True)
    password2 = forms.CharField(label='Confirm Password :', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'email':'Email:'}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            username = email.split('@')[0]
            if User.objects.filter(username=username).exists():
                raise ValidationError(f"The username '{username}' is already exists.")
            self.cleaned_data['username'] = username
        
        return email

    def save(self):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username'] 
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'basic_salary', 'work_hour']


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'data_of_join']