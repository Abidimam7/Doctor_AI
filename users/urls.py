# # users/urls.py

# from django.urls import path
# from . import views
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('', views.login_view, name='login'),  # Login page
#     path('register/', views.register, name='register'),
#     path('home/', views.home, name='home'),  # Home page
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
# ]

from django.urls import path
from .views import register, login_view, home, logout_view, update_about  # Import the update_about view

urlpatterns = [
    path('', home, name='home'),  # Set home as the default page
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),  # Logout path
    path('update_about/', update_about, name='update_about'),  # Add this line
]
