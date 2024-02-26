from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..models import Organization

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    organization_name = forms.CharField(max_length=100, required=True)  # Add organization name field
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','organization_name')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
            organization_name = self.cleaned_data['organization_name']
            Organization.objects.create(admin=user, name=organization_name)
        return user