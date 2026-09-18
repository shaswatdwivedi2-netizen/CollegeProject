"""
admin.py — Registers our models with Django's Admin Panel.

The Admin Panel is a built-in feature of Django.
After running the server, visit http://127.0.0.1:8000/admin
You can see ALL student records in a beautiful table interface —
search, filter, and even edit them — without writing any code!

To use it, first create a superuser:
    python manage.py createsuperuser
"""

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    This class tells Django HOW to display Students in the admin panel.
    """
    # Columns to show in the list view
    list_display = ['roll_number', 'full_name', 'branch', 'city', 'submitted_at']

    # Fields you can search by in the admin search box
    search_fields = ['roll_number', 'full_name', 'email', 'aadhar']

    # Sidebar filters in the admin panel
    list_filter = ['branch', 'gender', 'board_12']

    # Make submitted_at read-only (auto-generated, shouldn't be edited)
    readonly_fields = ['roll_number', 'submitted_at']
