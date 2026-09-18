"""
admissions/urls.py — URL patterns for the admissions app.

This file maps URLs to view functions.
When Django receives a request for a URL, it checks this file to find
which view function should handle that request.

Format:
    path('url-pattern/', view_function, name='nickname')

The 'name' is used in redirects and links — e.g. redirect('success', roll_number=...)
"""

from django.urls import path
from . import views   # Import all views from the same folder

urlpatterns = [

    # Home page — /
    path('', views.home, name='home'),

    # About Us page — /about
    path('about', views.about, name='about'),

    # Fee Structure page — /fees
    path('fees', views.fees, name='fees'),

    # Admission Form page — /form (shows the form)
    path('form', views.form_page, name='form'),

    # Form submission URL — /admissionform (receives POST data from the form)
    # This URL is set in form.html as: action="/admissionform"
    path('admissionform', views.submit_form, name='submit_form'),

    # Success page — /success/<roll_number>
    # <str:roll_number> is a URL parameter: Django captures whatever comes after /success/
    # and passes it to the success() view as the 'roll_number' argument
    path('success/<str:roll_number>', views.success, name='success'),

    # Student Details lookup page — /details
    path('details', views.student_lookup, name='student_lookup'),
]
