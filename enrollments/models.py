from django.db import models
from users.models import User
from courses.models import Course

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("registered", "Registered"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', limit_choices_to={'role':'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    registered_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="registered")
    certificate_issued = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')  # Prevent double-enroll

    def __str__(self):
        return f"{self.student.username} -> {self.course.name}"