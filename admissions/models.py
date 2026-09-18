"""
models.py — Defines the DATABASE TABLE for students.

A "model" in Django is a Python class that maps to a database table.
Each attribute (field) in the class becomes a COLUMN in the table.
Django reads this file and automatically creates the SQL table for us.
"""

from django.db import models


class Student(models.Model):
    """
    This class represents the 'student' table in SQLite.

    When we run 'python manage.py migrate', Django converts this Python class
    into an actual database table with the exact same columns.
    """

    # ── ROLL NUMBER ────────────────────────────────────────────────────────────
    # This is auto-generated, NOT filled by the student.
    # max_length=20 means the column can hold up to 20 characters.
    # unique=True means no two students can have the same roll number.
    roll_number = models.CharField(max_length=20, unique=True)

    # ── PERSONAL DETAILS (from Step 1 of the form) ────────────────────────────
    full_name   = models.CharField(max_length=200)
    dob         = models.DateField()               # Date of Birth: stores as YYYY-MM-DD
    gender      = models.CharField(max_length=10)
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    aadhar      = models.CharField(max_length=12)  # Exactly 12 digit Aadhar

    # ── CONTACT DETAILS (from Step 2 of the form) ─────────────────────────────
    email   = models.EmailField()                  # EmailField validates email format
    phone   = models.CharField(max_length=10)
    address = models.TextField()                   # TextField = long text (no length limit)
    city    = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    # ── ACADEMIC DETAILS (from Step 3 of the form) ────────────────────────────
    branch     = models.CharField(max_length=10)   # e.g. 'EE', 'IT', 'ME'
    jee_score  = models.FloatField(null=True, blank=True)  # Optional field
    board_12   = models.CharField(max_length=10)
    roll_12    = models.CharField(max_length=50)
    grade_12   = models.FloatField()               # 12th percentage
    grade_10   = models.FloatField()               # 10th percentage

    # ── METADATA ──────────────────────────────────────────────────────────────
    # auto_now_add=True means Django automatically saves the current date/time
    # when a new record is created. We don't need to set this manually.
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        This method tells Django what to display when showing a Student object.
        E.g. in the admin panel, it will show "0601EE260155 — Rahul Sharma"
        """
        return f"{self.roll_number} — {self.full_name}"

    class Meta:
        """
        Meta class lets us configure extra options for the table.
        ordering = ['-submitted_at'] means: newest student first by default.
        """
        ordering = ['-submitted_at']
