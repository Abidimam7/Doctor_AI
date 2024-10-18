# from django.contrib import admin
# from .models import PrePrompt
# from .models import Appointment

# class PrePromptAdmin(admin.ModelAdmin):
#     list_display = ('prompt_text', 'created_at')

# admin.site.register(PrePrompt, PrePromptAdmin)


# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ['doctor', 'patient', 'date', 'time', 'status']
#     list_filter = ['doctor', 'status', 'date']
#     search_fields = ['doctor__username', 'patient__username']

from django.contrib import admin
from .models import Diagnosis, PrePrompt, ChatSession, ChatMessage, Appointment

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_created', 'diagnosis']
    search_fields = ['user__username', 'diagnosis']
    list_filter = ['date_created']

@admin.register(PrePrompt)
class PrePromptAdmin(admin.ModelAdmin):
    list_display = ['prompt_text', 'created_at']
    search_fields = ['prompt_text']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp']
    search_fields = ['user__username']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'timestamp']
    search_fields = ['session__user__username', 'content']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'date', 'time', 'status']
    list_filter = ['doctor', 'status', 'date']
    search_fields = ['doctor__username', 'patient__username']
