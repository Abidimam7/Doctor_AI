# diagnosis/forms.py
from django import forms
from .models import Appointment
from users.models import CustomUser

class SymptomForm(forms.Form):
    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your symptoms here',
            'class': 'form-control',
            'rows': 5
        }),
        label="Describe your symptoms",
        max_length=1000,
        required=True
    )

    duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Number of days',
            'class': 'form-control',
        }),
        label="How many days have you experienced these symptoms?",
        required=True,
        min_value=1,
        max_value=365
    )

    severity = forms.ChoiceField(
        widget=forms.RadioSelect(),
        label="Severity of symptoms",
        choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')],
        required=True
    )

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']  # Include both date and time fields

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Only show doctors in the doctor dropdown
        self.fields['doctor'].queryset = CustomUser.objects.filter(role='doctor')
