# import openai
# import os
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from PIL import Image
# import pytesseract
# from .models import Diagnosis, ChatSession, ChatMessage, PrePrompt, CustomUser
# from .forms import SymptomForm
# import json
# import logging
# from pdfminer.high_level import extract_text as extract_pdf_text
# import PyPDF2

# import openai
# import os
# import logging
# import json
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from PIL import Image
# import pytesseract
# from .models import Diagnosis, ChatSession, ChatMessage, PrePrompt, CustomUser
# from .forms import SymptomForm
# import PyPDF2

# # Configure logging
# logger = logging.getLogger(__name__)

# # Set up Azure OpenAI API credentials
# openai.api_type = "azure"
# openai.api_key = os.getenv("AZURE_OPENAI_KEY")
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
# openai.api_version = "2024-02-01"

# # Function to generate diagnosis from Azure OpenAI
# def generate_diagnosis_from_openai(prompt):
#     print(f"Generating diagnosis for prompt: {prompt}")  # Print statement for debugging
#     try:
#         response = openai.Completion.create(
#             engine="gpt-35-turbo",  # Ensure this matches the engine in your Azure setup
#             prompt=prompt,
#             max_tokens=500,  # Adjust based on model requirements
#             temperature=0.7
#         )
#         if response.choices:
#             print(f"Diagnosis generated: {response.choices[0].text.strip()}")  # Print generated diagnosis
#             return response.choices[0].text.strip()
#         else:
#             logger.warning("Received no choices from OpenAI response.")
#             print("No choices received from OpenAI response.")  # Print warning
#             return "Unable to provide a diagnosis at this time."
#     except Exception as e:
#         logger.error(f"Error communicating with Azure OpenAI: {str(e)}")
#         print(f"Error communicating with Azure OpenAI: {str(e)}")  # Print error
#         return "Error processing the diagnosis. Please try again later."

# @csrf_exempt
# @login_required
# def get_diagnosis(request):
#     if request.user.role == 'doctor':
#         return redirect('doctor_dashboard')

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             symptoms = data.get('symptom')

#             if symptoms:
#                 # Fetch the latest pre-prompt from the database
#                 pre_prompt = PrePrompt.objects.latest('created_at').prompt_text
#                 prompt = f"{pre_prompt} Symptoms: {symptoms}."

#                 # Generate diagnosis using Azure OpenAI
#                 diagnosis_text = generate_diagnosis_from_openai(prompt)

#                 # Fetch relevant doctors based on the AI's diagnosis
#                 doctors = CustomUser.objects.filter(role='doctor', specialist__icontains=diagnosis_text).distinct()
#                 logger.info(f"Diagnosis response: {diagnosis_text}")
#                 logger.info(f"Doctors response: {[{'id': doctor.id, 'name': doctor.full_name, 'specialist': doctor.specialist} for doctor in doctors]}")



#                 return JsonResponse({
#                     'suggestion': diagnosis_text,
#                     'doctors': [{'id': doctor.id, 'name': doctor.full_name, 'specialist': doctor.specialist, 'location': doctor.location} for doctor in doctors],
#                     'error': None
#                 })

#             return JsonResponse({'error': 'No symptom provided'}, status=400)

#         except json.JSONDecodeError as json_error:
#             logger.error(f"JSON decode error: {str(json_error)}")
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#         except Exception as e:
#             logger.error(f"Error in get_diagnosis: {str(e)}")
#             return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)

#     if request.method == 'GET':
#         form = SymptomForm()
#         return render(request, 'diagnosis/diagnosis.html', {'form': form})

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# @csrf_exempt
# @login_required
# def upload_report(request):
#     if request.method == 'POST':
#         try:
#             report_file = request.FILES.get('report')

#             if not report_file:
#                 return JsonResponse({'error': 'No report file uploaded'}, status=400)

#             # Save the uploaded file temporarily
#             file_path = default_storage.save(f'temp_reports/{report_file.name}', report_file)
#             full_path = os.path.join(default_storage.location, file_path)

#             # Extract text from the file
#             if report_file.name.endswith('.pdf'):
#                 extracted_text = extract_pdf_text(full_path)
#             elif report_file.name.endswith(('.jpg', '.jpeg')):
#                 img = Image.open(full_path)
#                 extracted_text = pytesseract.image_to_string(img)
#             else:
#                 return JsonResponse({'error': 'Unsupported file type'}, status=400)

#             # Create a prompt for AI diagnosis
#             prompt = f"You are a doctor. Based on the following report content, provide a diagnosis or recommendation: {extracted_text}"

#             # Generate diagnosis using Azure OpenAI
#             diagnosis_text = generate_diagnosis_from_openai(prompt)

#             # Save the diagnosis to the database
#             diagnosis_instance = Diagnosis(user=request.user, symptoms=extracted_text, diagnosis=diagnosis_text)
#             diagnosis_instance.save()

#             # Optionally, create a chat session and save the AI response as a message
#             chat_session = ChatSession.objects.create(user=request.user)
#             ChatMessage.objects.create(session=chat_session, sender='AI', content=diagnosis_text)

#             # Clean up the temporary file
#             default_storage.delete(file_path)

#             # Return the diagnosis to the frontend
#             return JsonResponse({'suggestion': diagnosis_text, 'error': None})

#         except Exception as e:
#             logger.error(f"Error processing report: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)


# # Function to extract text from PDFs
# def extract_pdf_text(file_path):
#     text = ""
#     with open(file_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         for page in reader.pages:
#             text += page.extract_text() or ''
#     return text


# #