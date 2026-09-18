"""
views.py — Contains all PAGE LOGIC for the website.

A "view" in Django is a Python function that:
  1. Receives an HTTP request (when a user visits a URL)
  2. Does some work (query database, process form, generate roll number, etc.)
  3. Returns an HTTP response (renders an HTML page)

Think of views as the "bridge" between URLs and HTML templates.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student  # Import our Student model (database table)
import datetime


# ══════════════════════════════════════════════════════════════════════════════
#   SIMPLE PAGE VIEWS  (these just show HTML pages, no logic needed)
# ══════════════════════════════════════════════════════════════════════════════

def home(request):
    """
    Shows the Home page.
    'render' is a Django shortcut that finds the HTML file and sends it to the browser.
    """
    return render(request, 'home.html')


def about(request):
    """Shows the About Us page."""
    return render(request, 'about.html')


def fees(request):
    """Shows the Fee Structure page."""
    return render(request, 'fees.html')


def form_page(request):
    """
    Shows the Admission Form page (GET request only).
    When a user types /form in the browser, this function runs and shows the form.
    """
    return render(request, 'form.html')


# ══════════════════════════════════════════════════════════════════════════════
#   ROLL NUMBER GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_roll_number(branch):
    """
    Generates a unique roll number using this formula:
        COLLEGE_CODE + BRANCH + YEAR (2 digits) + SEQUENCE (4 digits)

    Example: 155th student, EE branch, admitted in 2026
        → 0601 + EE + 26 + 0155
        → 0601EE260155

    Steps:
    1. Count how many students already exist in the database
    2. Add 1 to get the new student's position
    3. Zero-pad it to 4 digits (e.g. 5 → 0005, 155 → 0155)
    4. Get the last 2 digits of the current year
    5. Combine everything
    """
    COLLEGE_CODE = '0601'

    # Count existing students. Student.objects.count() is Django's way of
    # running "SELECT COUNT(*) FROM student" in SQL.
    existing_count = Student.objects.count()

    # New student's sequence number (1-indexed, zero-padded to 4 digits)
    sequence = str(existing_count + 1).zfill(4)  # zfill(4) pads with zeros

    # Get last 2 digits of current year (e.g. 2026 → '26')
    year = str(datetime.datetime.now().year)[2:]

    # Build and return the roll number
    roll_number = f"{COLLEGE_CODE}{branch}{year}{sequence}"
    return roll_number


# ══════════════════════════════════════════════════════════════════════════════
#   FORM SUBMISSION VIEW
# ══════════════════════════════════════════════════════════════════════════════

def submit_form(request):
    """
    Handles the ADMISSION FORM when submitted (POST request).

    How a form submission works:
    1. User fills the form on /form page and clicks "Submit"
    2. The browser sends all form data to this URL via POST method
    3. Django receives it — request.POST is a dictionary of all form values
    4. We extract each field, generate a roll number, save to database
    5. We redirect the user to the success page with their roll number
    """

    # Only accept POST requests (form submissions)
    # If someone directly visits /admissionform in browser (GET), redirect home
    if request.method != 'POST':
        return redirect('home')

    # ── Extract form data from request.POST ───────────────────────────────────
    # request.POST is like a dictionary: {'fullName': 'Rahul', 'branch': 'EE', ...}
    # .get('fieldName', '') means: get the value, or use '' if it's missing

    # Personal Details
    full_name   = request.POST.get('fullName', '')
    dob         = request.POST.get('dob', '')
    gender      = request.POST.get('gender', '')
    father_name = request.POST.get('fatherName', '')
    mother_name = request.POST.get('motherName', '')
    aadhar      = request.POST.get('aadhar', '')

    # Contact Details
    email   = request.POST.get('email', '')
    phone   = request.POST.get('phone', '')
    address = request.POST.get('address', '')
    city    = request.POST.get('city', '')
    pincode = request.POST.get('pincode', '')

    # Academic Details
    branch    = request.POST.get('branch', '')
    jee_score = request.POST.get('jeeScore', None) or None  # Optional field
    board_12  = request.POST.get('board12', '')
    roll_12   = request.POST.get('roll12', '')
    grade_12  = request.POST.get('grade12', 0)
    grade_10  = request.POST.get('grade10', 0)

    # ── Generate Roll Number ───────────────────────────────────────────────────
    roll_number = generate_roll_number(branch)

    # ── Save to Database ───────────────────────────────────────────────────────
    # Student.objects.create() runs an SQL INSERT statement.
    # It creates a new row in the 'admissions_student' table.
    student = Student.objects.create(
        roll_number = roll_number,
        full_name   = full_name,
        dob         = dob,
        gender      = gender,
        father_name = father_name,
        mother_name = mother_name,
        aadhar      = aadhar,
        email       = email,
        phone       = phone,
        address     = address,
        city        = city,
        pincode     = pincode,
        branch      = branch,
        jee_score   = jee_score,
        board_12    = board_12,
        roll_12     = roll_12,
        grade_12    = float(grade_12),
        grade_10    = float(grade_10),
    )

    # ── Redirect to Success Page ──────────────────────────────────────────────
    # After saving, we send the user to /success/0601EE260155
    # This is a "POST-Redirect-GET" pattern to prevent form resubmission
    return redirect('success', roll_number=roll_number)


# ══════════════════════════════════════════════════════════════════════════════
#   SUCCESS PAGE VIEW
# ══════════════════════════════════════════════════════════════════════════════

def success(request, roll_number):
    """
    Shows the success page after form submission.

    'roll_number' is passed from the URL — e.g. /success/0601EE260155
    Django extracts '0601EE260155' from the URL and passes it to this function.

    We then pass it to the HTML template as 'roll_number' so the template
    can display it using {{ roll_number }}.
    """
    # 'context' is a dictionary of data we send to the HTML template
    context = {
        'roll_number': roll_number
    }
    return render(request, 'success.html', context)


# ══════════════════════════════════════════════════════════════════════════════
#   STUDENT LOOKUP VIEW
# ══════════════════════════════════════════════════════════════════════════════

def student_lookup(request):
    """
    Shows the Student Details lookup page at /details.

    This view handles TWO situations:
    1. User just visits /details → show the search box (student is None)
    2. User enters a roll number and clicks search → show their details

    How it knows which situation:
    - request.GET is a dictionary of URL query parameters
    - When user searches, the URL becomes /details?roll=0601EE260155
    - request.GET.get('roll') captures '0601EE260155' from the URL
    """
    student = None   # Default: no student found yet
    error = None     # Default: no error message
    roll_query = request.GET.get('roll', '').strip()  # Get the roll number from URL

    if roll_query:
        # User submitted a search — try to find the student in the database
        # Student.objects.filter() runs "SELECT * FROM student WHERE roll_number = '...'"
        # .first() returns the first result, or None if not found
        student = Student.objects.filter(roll_number=roll_query).first()

        if not student:
            # No student found with that roll number
            error = f"No student found with Roll Number: {roll_query}"

    # Pass both 'student' and 'error' to the template
    # If student is None → template shows the search form
    # If student is found → template shows all student details
    context = {
        'student': student,
        'error': error,
        'roll_query': roll_query,
    }
    return render(request, 'student.html', context)
