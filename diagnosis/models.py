# diagnosis/models.py
from django.conf import settings
from django.db import models
from users.models import CustomUser

class Diagnosis(models.Model):
    user = models.ForeignKey(CustomUser, related_name='diagnoses', on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis for {self.user.username} on {self.date_created}"

class PrePrompt(models.Model):
    prompt_text = models.TextField("Pre-Prompt", help_text="Enter the pre-prompt for AI responses")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pre-prompt added on {self.created_at}"

class ChatSession(models.Model):
    user = models.ForeignKey(CustomUser, related_name='chat_sessions', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat session for {self.user.username} on {self.timestamp}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)  # Can be "User" or "AI"
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Pending', 'Pending'),
    ]

    doctor = models.ForeignKey(CustomUser, related_name='appointments', on_delete=models.CASCADE)
    patient = models.ForeignKey(CustomUser, related_name='patient_appointments', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    def __str__(self):
        return f"Appointment with {self.patient.username} on {self.date} at {self.time}"
    
    
