from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    contact_no = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True, help_text="Total years of teaching/training experience")
    profile_picture = models.ImageField(upload_to="instructor_profiles/", null=True, blank=True)
    specialties = models.CharField(max_length=255, blank=True, help_text="Comma-separated areas of expertise")
    linkedin_url = models.URLField(blank=True)
    certifications = models.TextField(blank=True, help_text="Degrees, certificates, training etc.")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    age = models.IntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="student_profiles/", null=True, blank=True)
    education_level = models.CharField(max_length=100, blank=True, help_text="O/L, A/L, Diploma, etc.")
    occupation = models.CharField(max_length=100, blank=True, help_text="Student's current job if any")
    emergency_contact = models.CharField(max_length=100, blank=True)
    enrolled_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username