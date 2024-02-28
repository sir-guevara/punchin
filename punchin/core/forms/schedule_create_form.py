from django import forms
from ..models import Schedule, Shift


class ScheduleCreationForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['employee', 'location', 'shift', 'date']



class ShiftCreationForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['start_time', 'end_time', 'note']


