"""
URL configuration for healthcare_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users import views as user_views  # Import the users' views


urlpatterns = [
    path('admin/', admin.site.urls),  # This is for accessing the admin panel
    path('users/', include('users.urls')),  # Include user-related URLs
    path('diagnosis/', include('diagnosis.urls')),  # Include diagnosis-related URLs
    path('', user_views.register, name='home'),
]
