from django import forms
from ..models import Position


class PositionCreationForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'description',]


