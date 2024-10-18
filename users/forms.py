# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ['username', 'email', 'role', 'full_name', 'specialist', 'location', 'password1', 'password2']

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         # Set full_name, specialist, and location as not required by default
#         self.fields['full_name'].required = False
#         self.fields['specialist'].required = False
#         self.fields['location'].required = False

#     def clean(self):
#         cleaned_data = super().clean()
#         role = cleaned_data.get('role')

#         if role == 'doctor':
#             # Make doctor-specific fields required if the user is registering as a doctor
#             if not cleaned_data.get('full_name'):
#                 self.add_error('full_name', 'Full name is required for doctors.')
#             if not cleaned_data.get('specialist'):
#                 self.add_error('specialist', 'Specialist field is required for doctors.')
#             if not cleaned_data.get('location'):
#                 self.add_error('location', 'Location field is required for doctors.')

#         return cleaned_data

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. First Name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Last Name')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'specialist', 'location', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Set specialist and location as not required by default
        self.fields['specialist'].required = False
        self.fields['location'].required = False

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'doctor':
            # Make doctor-specific fields required if the user is registering as a doctor
            if not cleaned_data.get('specialist'):
                self.add_error('specialist', 'Specialist field is required for doctors.')
            if not cleaned_data.get('location'):
                self.add_error('location', 'Location field is required for doctors.')

        return cleaned_data
