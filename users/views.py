from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import JsonResponse


def register(request):
    # If the user is already logged in, redirect them to their dashboard or another page
    if request.user.is_authenticated:
        if request.user.role == 'doctor':
            return redirect('doctor_dashboard')
        else:
            return redirect('diagnosis')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not save yet
            user.first_name = form.cleaned_data.get('first_name')  # Set first name
            user.last_name = form.cleaned_data.get('last_name')    # Set last name
            user.role = form.cleaned_data.get('role')              # Set user role
            user.save()  # Save the user now

            role = form.cleaned_data.get('role')

            if role == 'doctor':
                # Set doctor-specific fields
                user.specialist = form.cleaned_data.get('specialist')
                user.location = form.cleaned_data.get('location')
                user.save()  # Save the doctor-specific fields

                # Log the user in after successful registration
                login(request, user)

                # Redirect to the doctor dashboard
                return redirect('doctor_dashboard')

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # For patients, redirect to login after registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

# Login function
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Check if the user is a doctor or patient
                if user.role == 'doctor':
                    # Redirect doctors to the doctor dashboard
                    return redirect('doctor_dashboard')
                else:
                    # Redirect patients to the diagnosis page (Doctor AI)
                    return redirect('diagnosis')

            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

# Home function
def home(request):
    return render(request, 'home.html')

# Logout function
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the homepage after logging out




@login_required
def update_about(request):
    doctor = request.user  # Assuming the logged-in user is a doctor
    if request.method == 'POST':
        about = request.POST.get('about')
        doctor.about = about  # Update the about field
        doctor.save()
        return JsonResponse({'success': True})  # Return success response
    return JsonResponse({'success': False}, status=400)  # Return error response if not POST






