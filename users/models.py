from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    SPECIALIST_CHOICES = [
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Surgeon', 'Surgeon'),
        ('General Physician', 'General Physician'),
        ('Gastroenterologist', 'Gastroenterologist'),
        ('Other', 'Other')
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)  # Doctor or Patient
    full_name = models.CharField(max_length=255, blank=True, null=True)  # Doctor full name
    specialist = models.CharField(max_length=100, choices=SPECIALIST_CHOICES, blank=True, null=True)  # Dropdown specialist choices
    location = models.CharField(max_length=255, blank=True, null=True)  # Doctor's location (city, hospital, etc.)
    about = models.TextField(blank=True, null=True) 
    
    def is_doctor(self):
        return self.role == 'doctor'


    class Meta:
        permissions = (("can_view_profile", "Can View Profile"),)

    # Add these fields if needed
    patient_history = models.TextField(blank=True, null=True)
