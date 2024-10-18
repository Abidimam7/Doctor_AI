from django.shortcuts import render, redirect, get_object_or_404
from .forms import SymptomForm
from django.contrib.auth.decorators import login_required, user_passes_test
from api.services.gemini_service import GeminiAPI  # Assuming you're using Gemini API
from django.http import JsonResponse
import google.generativeai as genai
from .models import Diagnosis, PrePrompt,Diagnosis, Appointment, ChatSession, ChatMessage
from users.models import CustomUser
import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from pdfminer.high_level import extract_text as extract_pdf_text
import pytesseract  # OCR for JPG
from PIL import Image
import logging
from django.contrib import messages


# Configure logging
logger = logging.getLogger(__name__)

# Configure the API with your API key
genai.configure(api_key=os.getenv("API_KEY"))

@csrf_exempt  # Ensure CSRF protection is managed properly
@login_required
def get_diagnosis(request):
    if request.user.role == 'doctor':
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            symptoms = data.get('symptom')

            if symptoms:
                pre_prompt = PrePrompt.objects.latest('created_at').prompt_text
                prompt = f"{pre_prompt} Symptoms: {symptoms}."
                model = genai.GenerativeModel("gemini-1.5-pro-002")
                response = model.generate_content(prompt)

                diagnosis_text = (response.candidates[0].content.parts[0].text 
                                  if response.candidates and response.candidates[0].content.parts 
                                  else "No suggestion received.")

                doctors = CustomUser.objects.filter(role='doctor', specialist__icontains=diagnosis_text).distinct()
                
                return JsonResponse({
                    'suggestion': diagnosis_text,
                    'doctors': [{'id': doctor.id, 'name': doctor.first_name, 'specialist': doctor.specialist, 'location': doctor.location} for doctor in doctors],
                    'error': None
                })

            return JsonResponse({'error': 'No symptom provided'}, status=400)

        except json.JSONDecodeError as json_error:
            logger.error(f"JSON decode error: {str(json_error)}")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error(f"Error in get_diagnosis: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)

    if request.method == 'GET':
        form = SymptomForm()
        return render(request, 'diagnosis/diagnosis.html', {'form': form})

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# Set the path to the Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@csrf_exempt
@login_required
def upload_report(request):
    if request.method == 'POST':
        try:
            report_file = request.FILES.get('report')

            if not report_file:
                return JsonResponse({'error': 'No report file uploaded'}, status=400)

            # Save the uploaded file temporarily
            file_path = default_storage.save(f'temp_reports/{report_file.name}', report_file)
            full_path = os.path.join(default_storage.location, file_path)

            # Extract text from the file
            if report_file.name.endswith('.pdf'):
                extracted_text = extract_pdf_text(full_path)  # Make sure this function is defined
            elif report_file.name.endswith(('.jpg', '.jpeg')):
                img = Image.open(full_path)
                extracted_text = pytesseract.image_to_string(img)
            else:
                return JsonResponse({'error': 'Unsupported file type'}, status=400)

            # Create a prompt for AI diagnosis
            prompt = f"You are a doctor. Based on the following report content, provide a diagnosis or recommendation: {extracted_text}"

            # Call the generative model to get the diagnosis
            model = genai.GenerativeModel("gemini-1.5-pro-002")
            response = model.generate_content(prompt)

            # Get the diagnosis text from the response
            if response.candidates and response.candidates[0].content.parts:
                diagnosis_text = response.candidates[0].content.parts[0].text
            else:
                diagnosis_text = "No suggestion received."

            # Save the diagnosis to the database
            diagnosis_instance = Diagnosis(user=request.user, symptoms=extracted_text, diagnosis=diagnosis_text)
            diagnosis_instance.save()

            # Optionally, create a chat session and save the AI response as a message
            chat_session = ChatSession.objects.create(user=request.user)
            ChatMessage.objects.create(session=chat_session, sender='AI', content=diagnosis_text)

            # Clean up the temporary file
            default_storage.delete(file_path)

            # Return the diagnosis to the frontend
            return JsonResponse({'suggestion': diagnosis_text, 'error': None})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

import PyPDF2

def extract_pdf_text(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ''
    return text


# Function to check if the user is a doctor
def is_doctor(user):
    return user.role == 'doctor'

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    # Fetch the doctor's appointments and diagnoses
    appointments = Appointment.objects.filter(doctor=request.user).order_by('-date')
    diagnoses_by_patient = {}

    # Fetch all diagnoses for patients assigned to this doctor
    for appointment in appointments:
        patient_diagnoses = Diagnosis.objects.filter(user=appointment.patient).order_by('-date_created')
        if patient_diagnoses.exists():
            diagnoses_by_patient[appointment.patient] = patient_diagnoses

    # Pass doctor details, appointments, and diagnoses to the template
    return render(request, 'diagnosis/doctor_dashboard.html', {
        'doctor': request.user,  # Doctor details
        'appointments': appointments,
        'diagnoses_by_patient': diagnoses_by_patient,
    })



@login_required
def book_appointment(request, doctor_id=None):
    # Fetch the list of doctors for the dropdown in case the doctor_id is not provided
    doctors = CustomUser.objects.filter(role='doctor')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if doctor_id and date and time:
            # Fetch the doctor and current patient (logged-in user)
            doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
            patient = request.user

            # Check if the time slot is already taken
            if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
                messages.error(request, 'This time slot is already booked. Please choose another time.')
            else:
                # Create and save the appointment
                appointment = Appointment.objects.create(doctor=doctor, patient=patient, date=date, time=time)
                appointment.save()
                messages.success(request, 'Your appointment has been successfully booked!')
                return redirect('patient_history')  # Redirect to patient dashboard after booking

        else:
            messages.error(request, 'Please fill in all fields.')

    context = {
        'doctors': doctors,
        'selected_doctor_id': doctor_id  # Pass the selected doctor (if any)
    }
    return render(request, 'diagnosis/book_appointment.html', context)
@login_required
def cancel_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id, patient=request.user)  # Ensure the appointment belongs to the logged-in user
        appointment.delete()  # Delete the appointment
        messages.success(request, 'Your appointment has been successfully cancelled!')
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found or you do not have permission to cancel this appointment.')

    return redirect('patient_history')  # Redirect back to the patient history


@login_required
def patient_history(request):
    # Fetch diagnoses for the logged-in patient
    diagnoses = Diagnosis.objects.filter(user=request.user).order_by('-date_created')
    
    # Fetch appointments for the logged-in patient
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date')

    # Fetch chat sessions for the logged-in patient and prefetch messages for optimization
    chat_sessions = ChatSession.objects.filter(user=request.user).prefetch_related('messages').order_by('-timestamp')

    # Add a success message if there's any specific action (e.g., after booking an appointment)
    if 'appointment_success' in request.GET:
        messages.success(request, 'Your appointment has been successfully booked!')

    return render(request, 'diagnosis/patient_history.html', {
        'diagnoses': diagnoses,
        'appointments': appointments,
        'chat_sessions': chat_sessions,  # Pass chat sessions to the template
    })

@login_required
def delete_chat_session(request, session_id):
    if request.method == 'POST':
        # Get the chat session to delete
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        
        # Delete the session and all its related messages
        session.delete()
        
        # Add a success message
        messages.success(request, 'Chat session deleted successfully.')
        
        # Redirect back to the patient history page
        return redirect('patient_history')
    
@login_required
def patient_dashboard(request):
    # Fetch the appointments for the logged-in user
    appointments = Appointment.objects.filter(patient=request.user)

    context = {
        'appointments': appointments
    }
    return render(request, 'diagnosis/patient_dashboard.html', context)

@csrf_exempt
@login_required
def save_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('content')
        session_id = request.POST.get('session_id')

        # Retrieve or create a session
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(user=request.user)

        # Save the message
        chat_message = ChatMessage(session=session, sender=request.user.username, content=message_content)
        chat_message.save()

        return JsonResponse({'status': 'success', 'message': 'Message saved successfully!', 'session_id': session.id})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

@login_required
def chat_view(request):
    session = ChatSession.objects.filter(user=request.user).last()
    messages = session.messages.all() if session else []

    return render(request, 'diagnosis/chat.html', {'messages': messages})

@login_required
def save_chat_session(request):
    if request.method == 'POST':
        user = request.user  # Assuming you have user authentication set up
        data = json.loads(request.body)  # Load JSON data from the request body

        # Get message and response from the received JSON
        message_content = data.get('message')
        response_content = data.get('response')
        
        # Create a new chat session
        chat_session = ChatSession.objects.create(user=user)

        # Save individual chat messages
        ChatMessage.objects.create(session=chat_session, sender='User', content=message_content)
        ChatMessage.objects.create(session=chat_session, sender='AI', content=response_content)

        # Return a success response as JSON
        return JsonResponse({'status': 'success', 'session_id': chat_session.id})

    # If the request is not POST, return an error response
    return JsonResponse({'error': 'Invalid request'}, status=400)

from collections import defaultdict

def chat_history_view(request):
    user = request.user  # Assuming user is logged in
    chat_sessions = ChatSession.objects.filter(user=user).order_by('-timestamp')  # Order by latest session first

    # Create a dictionary to hold messages grouped by date
    chat_history = defaultdict(list)

    for session in chat_sessions:
        messages = session.messages.all().order_by('timestamp')  # Sort messages by timestamp
        # Group messages by date
        for message in messages:
            date_key = message.timestamp.date()  # Use the date part as the key
            chat_history[date_key].append(message)

    # Convert to a list of tuples for easier template rendering
    grouped_chat_history = sorted(chat_history.items(), key=lambda item: item[0], reverse=True)  # Sort by date descending

    context = {
        'grouped_chat_history': grouped_chat_history,
    }
    return render(request, 'chat_history.html', context)

@login_required
def chat_session_detail_view(request, session_id):
    chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    chat_messages = chat_session.messages.all()  # Fetch all messages for the session

    context = {
        'chat_session': chat_session,
        'chat_messages': chat_messages,
    }
    return render(request, 'chat_session_detail.html', context)


