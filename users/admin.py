# diagnosis/admin.py
from django.contrib import admin
from users.models import CustomUser  # Ensure you import the CustomUser model

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email', 'role', 'specialist', 'location']  # Fields to display
    list_filter = ['role']  # Filter by role (doctor/patient)
    search_fields = ['username', 'full_name', 'email']  # Enable search

    def get_queryset(self, request):
        # Get the original queryset
        qs = super().get_queryset(request)
        return qs  # Show all users (doctors and patients)

    def has_view_permission(self, request, obj=None):
        # Ensure that only admins can view this section
        return request.user.is_superuser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email', 'role', 'specialist', 'location']  # Fields to display
    list_filter = ['role']  # Filter by role (doctor/patient)
    search_fields = ['username', 'full_name', 'email']  # Enable search

    def get_queryset(self, request):
        # Get the original queryset
        qs = super().get_queryset(request)
        return qs  # Show all users (doctors and patients)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


