from django import forms
from django.contrib.auth.models import User
from ..models import Employee
import string,random

class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['phone_number', 'address', 'primary_color', 'secondary_color', 'position', 'hourly_rate', 'overtime_hourly_rate',]


  
class UserCreationForm(forms.ModelForm):
    def generate_password(self):
        length = 10
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    def save(self, commit=True):
        user = super().save(commit=False)
        cpassword =  self.generate_password()
        print(cpassword)
        user.set_password(cpassword)  # Set a random password
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
