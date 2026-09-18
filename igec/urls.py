"""
igec/urls.py — The ROOT URL configuration for the entire project.

Django starts here when any request comes in.
We tell it to forward ALL URLs to our 'admissions' app's urls.py.

include() means: "look in admissions/urls.py for the actual URL matching"
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django's built-in admin panel at /admin
    # Visit http://127.0.0.1:8000/admin to see all students in a GUI
    path('admin/', admin.site.urls),

    # Everything else goes to our admissions app's urls.py
    # '' means: forward all URLs starting from the root
    path('', include('admissions.urls')),
]
