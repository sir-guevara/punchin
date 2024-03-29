from django import forms
from ..models import Location


class LocationCreationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'longitude', 'latitude','address']


