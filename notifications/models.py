from django.db import models

class Notification(models.Model):
    NOTIFY_TYPES = [
        ("batch", "Batch"),
        ("holiday", "Holiday"),
        ("seminar", "Seminar"),
        ("jobfair", "Job Fair"),
        ("general", "General"),
    ]
    title = models.CharField(max_length=200)
    body = models.TextField()
    notify_type = models.CharField(max_length=50, choices=NOTIFY_TYPES, default="general")
    target_role = models.CharField(max_length=20, blank=True)  # Example: 'student', 'instructor', etc (or comma separated)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.notify_type}"