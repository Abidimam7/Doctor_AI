# from django.urls import path
# from . import views  # Importing views module

# urlpatterns = [
#     path('', views.get_diagnosis, name='diagnosis'),  # Diagnosis page
#     path('history/', views.patient_history, name='patient_history'),
#     path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
#     path('upload-report/', views.upload_report, name='upload_report'),  # New route for report upload
#     path('book-appointment/', views.book_appointment, name='book_appointment'),  # Corrected reference
#     path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),  # Cancellation route
#     path('save_message/', views.save_message, name='save_message'),  # URL to save messages
#     path('chat/', views.chat_view, name='chat_view'),  # Chat view
#     path('save-chat-session/', views.save_chat_session, name='save_chat_session'),  # Add this line if missing
#     path('dashboard/', views.patient_dashboard, name='patient_dashboard'),  # Patient Dashboard
#     path('chat/delete/<int:message_id>/', views.delete_chat_message, name='delete_chat_message'),  # New URL for deleting chat messages
    
# ]
from django.urls import path
from . import views  # Importing views module

urlpatterns = [
    # Diagnosis and history-related routes
    path('', views.get_diagnosis, name='diagnosis'),  # Diagnosis page
    path('history/', views.patient_history, name='patient_history'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('upload-report/', views.upload_report, name='upload_report'),  # New route for report upload

    # Appointment-related routes
    path('book-appointment/', views.book_appointment, name='book_appointment'),  # Appointment booking
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),  # Cancellation route

    # Chat-related routes
    path('save_message/', views.save_message, name='save_message'),  # URL to save messages
    path('chat/', views.chat_view, name='chat_view'),  # Chat view
    path('save-chat-session/', views.save_chat_session, name='save_chat_session'),  # Saving chat sessions
    path('chat/delete-session/<int:session_id>/', views.delete_chat_session, name='delete_chat_session'),  # Deleting chat sessions

    # Dashboard route
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),  # Patient Dashboard
]


