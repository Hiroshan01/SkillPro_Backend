import uuid

from courses.models import Course
from django.db import models
from enrollments.models import Enrollment
from users.models import User


class Certificate(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("issued", "Issued"),
        ("revoked", "Revoked"),
    ]

    enrollment = models.OneToOneField(
        Enrollment, on_delete=models.CASCADE, related_name="certificate"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="certificates"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="certificates"
    )
    certificate_number = models.CharField(
        max_length=50,
        unique=True,
        default=uuid.uuid4,  # <-- Changed: auto-generate unique ID
        editable=False,
    )
    issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    grade = models.CharField(max_length=5, blank=True, help_text="A, B, C, D, etc.")
    certificate_file = models.FileField(
        upload_to="certificates/",
        null=True,
        blank=True,
        help_text="PDF or image of the certificate",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.name} ({self.certificate_number})"

    class Meta:
        ordering = ["-issue_date"]
